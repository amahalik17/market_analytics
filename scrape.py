import pandas as pd
import bs4 as bs
import requests
import os

html = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
soup = bs.BeautifulSoup(html.text)


tickers = []
names = []


table = soup.find('table', {'class': 'wikitable sortable'})
rows = table.findAll('tr')[1:]


for row in rows:
    ticker = row.findAll('td')[0].text
    tickers.append(ticker[:-1])


for row in rows:
    name = row.findAll('td')[1].text
    names.append(name[:-1])


df = pd.DataFrame(list(zip(tickers, names)))
df.columns = ['Ticker', 'Name']


print(df)

# Ensure the directory exists
output_dir = 'Market_Data'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


# Save the DataFrame to a CSV file
df.to_csv(os.path.join(output_dir, 'sp500_list.csv'), index=False)


