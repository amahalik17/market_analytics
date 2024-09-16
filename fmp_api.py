# import dependencies
import requests
import pandas as pd
from config import API_KEY



historical_data ='historical-price-full'

ticker ='AAPL'

base_url = 'https://financialmodelingprep.com/api'

url = f'{base_url}/v3/{historical_data}/{ticker}?apikey={API_KEY}'

# print(url)

response = requests.get(url)

data = response.json()

df = pd.DataFrame(data).T

print(df)

