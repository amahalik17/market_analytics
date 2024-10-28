# Import dependencies
import psycopg2
from psycopg2 import sql
import pandas as pd
from config import db_pw


# Function to connect to the PostgreSQL database
def connect_to_db():
    conn = psycopg2.connect(
        host="localhost",
        database="market_data",
        user="postgres",
        password=db_pw
    )
    return conn


# Function to insert data into the PostgreSQL database
def insert_data(df):
    try:
        conn = psycopg2.connect(dbname='market_data', user='postgres', password=db_pw, host='localhost')
        cursor = conn.cursor()
        
        # Using executemany for batch insert
        # Dont forget to change table name or layout if neccessary before running script
        insert_query = '''
            INSERT INTO fav_stocks (ticker, date, open, high, low, close, volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (ticker, date) DO NOTHING;
        '''
        
        # Convert DataFrame to a list of tuples
        data_to_insert = list(df.itertuples(index=False, name=None))

        cursor.executemany(insert_query, data_to_insert)
        conn.commit()
        cursor.close()
        conn.close()
        
        print("Data inserted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Function to fetch data from the PostgreSQL database
def fetch_price_data(ticker, limit=50, start_date=None, end_date=None):
    try:
        conn = connect_to_db()
        query = '''
            SELECT date, close
            FROM fav_stocks
            WHERE ticker = %s
        '''
        params = [ticker]

        # Filter by date range if provided
        if start_date and end_date:
            query += ' AND date BETWEEN %s AND %s'
            params.extend([start_date, end_date])
        elif start_date:
            query += ' AND date >= %s'
            params.append(start_date)
        elif end_date:
            query += ' AND date <= %s'
            params.append(end_date)

        
        # Add the limit to the query
        query += ' ORDER BY date DESC LIMIT %s'
        params.append(limit)
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()

        # Sort by date if not already sorted
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values(by='date').reset_index(drop=True)
        
        return df
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


