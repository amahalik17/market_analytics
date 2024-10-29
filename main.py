# Import dependencies
import pandas as pd
from datetime import datetime, date
import requests
from auth import get_access_token
from db import insert_data, fetch_price_data
from indicators import calculate_rsi, rsi_divergence


# # Set display options for viewing full DataFrames
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)

# Read the CSV file into a DataFrame
tickers_names_df = pd.read_csv('Market_Data/sp500_list.csv')

# turn csv columns into lists
tickers_list = tickers_names_df['Ticker'].tolist()

# Test with smaller list at first
fav_tickers_list = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'TSLA', 'AMD', 'NVDA', 'NFLX', 'META', 'CVS', 'JPM', 'SQ', 'LMT', 'CVX']
fund_tickers_list = ['SPY', 'QQQ', 'IWM', 'DIA', 'GLD', 'VXX']

# Get the access token from auth.py
access_token = get_access_token()

# Set the base URL for the price history endpoint
base_url = 'https://api.schwabapi.com/marketdata/v1'

# # Endpoints for future use
# price_history_url = f'{base_url}/pricehistory?symbol={ticker}&periodType=month'
# one_yr_url = f'{base_url}/pricehistory?symbol={ticker}&periodType=year&frequencyType=daily'
# three_month_url = f'{base_url}/pricehistory?symbol={ticker}&periodType=month&period=3&frequencyType=daily'


# Add Authorization header with the access token
headers = {
    'Authorization': f'Bearer {access_token}'
}

# Create an empty list to store all the data
all_data = []

# Iterate through the list of tickers and fetch price history for each
for ticker in fav_tickers_list:
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


def rsi_df():

    # Loop over each ticker and calculate RSI
    for ticker in fav_tickers_list:
        # Get price data for the ticker
        price_data = fetch_price_data(ticker, limit=50)
        # Calculate RSI
        rsi = calculate_rsi(price_data).dropna()
        print(f"RSI for {ticker}:")
        print(rsi)



def rsi_divergence_df():
    
    all_divergences = []

    # Loop through each ticker in list
    for ticker in fav_tickers_list:
        # Fetch price data for the ticker
        price_data = fetch_price_data(ticker, limit=50)
        # Check if we have enough data
        if price_data is not None and len(price_data) >= 14:
            # Calculate RSI divergence
            divergence_df = rsi_divergence(price_data, ticker, period=14)
            # Append to the list if divergences are found
            if not divergence_df.empty:
                all_divergences.append(divergence_df)

    # Combine all divergence data into a single DataFrame
    if all_divergences:
        combined_divergences = pd.concat(all_divergences, ignore_index=True)
        print(combined_divergences)
    else:
        print("No divergences found.")




# Main function to call your loops or add additional logic
def main():
    rsi_df()
    #rsi_divergence_df()


if __name__ == "__main__":
    main()
