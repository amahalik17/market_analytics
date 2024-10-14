

# Stock Market Data Analytics

## About The Project
This project is currently being worked on and will continue to be pushed as progress is made. What I have done so far:


- Establish a connection the the Charles Schwab API by getting
an access token, using an API KEY and SECRET KEY (auth.py)

- Web scraped a list of current S+P500 companies and saved them as a csv file (scrape.py)

- Create python list(s) of stocks or funds to request historical data for (main.py)

- Make API requests and convert json data into pandas dataframe (main.py)

- Format the datetime object to human readable date (main.py)

- Using pgadmin, create a postgres SQL database and create tables to hold the data (queries.sql)

- Establish connection to the postgres database and create a function to insert API data into it (db.py)

- Inserted the data into my database

## Language
-Python

## Packages and Libraries
- TA-Lib
- psycopg2
- pandas
- numpy
- bs4
- requests
- datetime

