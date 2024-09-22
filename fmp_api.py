# import dependencies
import requests
import pandas as pd
from config import API_KEY
from datetime import datetime, date


historical_data ='historical-price-full'
quote_data ='quote'

ticker ='AAPL'

# today = datetime.today().strftime('%Y-%m-%d')
# todays_date = date.today()
# print(todays_date)
# print(today)
# date_to = today
date_from = '2024-01-01'




base_url = 'https://financialmodelingprep.com/api'
historical_url = f'{base_url}/v3/{historical_data}/{ticker}?from={date_from}&apikey={API_KEY}'
quote_url = f'{base_url}/v3/{quote_data}/{ticker}?apikey={API_KEY}'

# print(historical_url)
# print(quote_url)

response = requests.get(historical_url)
data = response.json()
# print(data)

df = pd.DataFrame(data, index=None)
# print(df)
