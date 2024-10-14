# Import dependencies
import psycopg2
from psycopg2 import sql
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


def insert_data(df):
    try:
        conn = psycopg2.connect(dbname='market_data', user='postgres', password=db_pw, host='localhost')
        cursor = conn.cursor()
        
        # Using executemany for batch insert
        # Dont forget to change table name or layout if neccessary before running script
        insert_query = '''
            INSERT INTO table_name (ticker, date, open, high, low, close, volume)
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
