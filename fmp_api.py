# import dependencies
import requests
import pandas as pd
from config import API_KEY
from datetime import datetime


historical_data ='historical-price-full'
quote_data ='quote'

ticker ='AAPL'

today = datetime.today().strftime('%Y-%m-%d')
# print(today)
# date_from = '2020-01-01'
# date_to = today

base_url = 'https://financialmodelingprep.com/api'
historical_url = f'{base_url}/v3/{historical_data}/{ticker}?apikey={API_KEY}'
quote_url = f'{base_url}/v3/{quote_data}/{ticker}?apikey={API_KEY}'

# print(historical_url)
# print(quote_url)

response = requests.get(historical_url)

data = response.json()

df = pd.DataFrame(data).T

# print(df)
