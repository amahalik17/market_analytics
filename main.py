# Import dependencies
import pandas as pd
from datetime import datetime, date
import requests
from auth import get_access_token



# Test with smaller list at first
# tickers_list = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']


# Read the CSV file into a DataFrame
tickers_names_df = pd.read_csv('Market_Data/sp500_list.csv')

# turn csv columns into lists
tickers_list = tickers_names_df['Ticker'].tolist()
names_list = tickers_names_df['Name'].tolist()
# print(tickers_list)
# print(names_list)


# Get the access token from auth.py
access_token = get_access_token()

# Set the base URL for the price history endpoint
base_url = 'https://api.schwabapi.com/marketdata/v1'

# Add Authorization header with the access token
headers = {
    'Authorization': f'Bearer {access_token}'
}

# Iterate through the list of tickers and fetch price history for each
for ticker in tickers_list:
    price_history_url = f'{base_url}/pricehistory?symbol={ticker}&periodType=month'
    
    # Make the API request
    response = requests.get(price_history_url, headers=headers)
    
    # Check the response
    if response.status_code == 200:
        data = response.json()
        print(f"Price history for {ticker}:", data)
    else:
        print(f"Failed to retrieve data for {ticker}: {response.status_code}")






























# Initialize an empty DataFrame to hold all tickers' data
# all_tickers_data = pd.DataFrame()

# Iterate through the list of tickers
# for ticker in tickers_list:
#     quote_url = f'{base_url}/v3/{quote_data}/{ticker}?apikey={API_KEY}'
#     response = requests.get(quote_url)
#     data = response.json()

# print(data)
# After the loop, print the combined DataFrame
# print(all_tickers_data)

# Optionally save to a CSV file
# all_tickers_data.to_csv('all_tickers_data.csv', index=False)