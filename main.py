# Import dependencies
import pandas as pd
from datetime import datetime, date
import requests
from auth import get_access_token
from db import insert_data


# Test with smaller list at first
# fav_tickers_list = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'TSLA', 'AMD', 'NVDA', 'NFLX', 'META', 'CVS', 'JPM', 'SQ', 'LMT', 'CVX']
# fund_tickers_list = ['SPY', 'QQQ', 'IWM', 'DIA', 'GLD', 'VXX']

# Read the CSV file into a DataFrame
tickers_names_df = pd.read_csv('Market_Data/sp500_list.csv')

# turn csv columns into lists
tickers_list = tickers_names_df['Ticker'].tolist()
# names_list = tickers_names_df['Name'].tolist()
# # print(tickers_list)
# # print(names_list)

# Get the access token from auth.py
access_token = get_access_token()

# Set the base URL for the price history endpoint
base_url = 'https://api.schwabapi.com/marketdata/v1'

# Add Authorization header with the access token
headers = {
    'Authorization': f'Bearer {access_token}'
}

# Endpoints for future use
# price_history_url = f'{base_url}/pricehistory?symbol={ticker}&periodType=month'
# one_yr_url = f'{base_url}/pricehistory?symbol={ticker}&periodType=year&frequencyType=daily'
# three_month_url = f'{base_url}/pricehistory?symbol={ticker}&periodType=month&period=3&frequencyType=daily'

# Create an empty list to store all the data
all_data = []

# Iterate through the list of tickers and fetch price history for each
for ticker in tickers_list:
    one_yr_url = f'{base_url}/pricehistory?symbol={ticker}&periodType=year&period=1&frequencyType=daily&needExtendedHoursData=false&needPreviousClose=false'
    # Make the API request
    response = requests.get(one_yr_url, headers=headers)
    
    # Check the response
    if response.status_code == 200:
        json_data = response.json()
        # print(f"Price history for {ticker}:", json_data)

        # Extract the price data
        price_data = json_data.get('candles', [])
        
        # Add a 'ticker' column to track which data belongs to which ticker
        for x in price_data:
            x['ticker'] = ticker
        
        # Append the candles to the all_data list
        all_data.extend(price_data)
    else:
        print(f"Failed to retrieve data for {ticker}: {response.status_code}")



# Convert the collected data into a Pandas DataFrame
df = pd.DataFrame(all_data)

# Convert the epoch 'datetime' to human-readable dates
df['date'] = pd.to_datetime(df['datetime'], unit='ms').dt.strftime('%m-%d-%Y')

# Drop the original 'datetime' column as we now have a formatted 'date' column
df = df.drop(columns=['datetime'])

# Reorder the columns to match the table schema
df = df[['ticker', 'date', 'open', 'high', 'low', 'close', 'volume']]

# Convert columns to appropriate types
df['open'] = df['open'].astype(float)
df['high'] = df['high'].astype(float)
df['low'] = df['low'].astype(float)
df['close'] = df['close'].astype(float)
df['volume'] = df['volume'].astype(int)

# print(df)

# Insert the data into the PostgreSQL db
insert_data(df)

