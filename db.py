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


def insert_data(df):
    # SQL query to insert data, with ON CONFLICT to avoid duplicate entries
    insert_query = """
        INSERT INTO price_history (ticker, date, open, high, low, close, volume)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (ticker, date) DO NOTHING;
    """

    # Convert DataFrame rows into a list of tuples
    data_to_insert = df.to_records(index=False)

    # Connect to the database
    conn = connect_to_db()
    cur = conn.cursor()

    try:
        # Execute many insert queries at once
        cur.executemany(insert_query, data_to_insert)
        conn.commit()  # Commit the transaction
        print(f"{cur.rowcount} rows were inserted into the database.")
    except Exception as e:
        conn.rollback()  # Rollback in case of any error
        print(f"An error occurred: {e}")
    finally:
        cur.close()
        conn.close()



# def insert_data(df):
#     # Connect to the database
#     conn = connect_to_db()
#     cursor = conn.cursor()

#     try:
#         # Iterate over each row in the DataFrame
#         for index, row in df.iterrows():
#             # SQL query to insert data, with a conflict check
#             insert_query = """
#                 INSERT INTO price_history (ticker, date, open, high, low, close, volume)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s)
#                 ON CONFLICT (ticker, date) DO NOTHING;
#             """
            
#             # Execute the insert query
#             cursor.execute(insert_query, (row['ticker'], row['date'], row['open'], row['high'], row['low'], row['close'], row['volume']))

#         conn.commit()  # Commit the transaction
#         print(f"{df.shape[0]} rows were inserted into the database.")
        
#     except Exception as e:
#         conn.rollback()  # Rollback in case of any error
#         print(f"An error occurred: {e}")
        
#     finally:
#         cursor.close()
#         conn.close()





# # Function to insert DataFrame into the price_history table
# def insert_data(df):
#     conn = connect_to_db()
#     cursor = conn.cursor()

#     for index, row in df.iterrows():
#         cursor.execute("""
#             INSERT INTO price_history (ticker, date, open, high, low, close, volume)
#             VALUES (%s, %s, %s, %s, %s, %s, %s)
#         """, (
#             row['ticker'], row['date'], row['open'], row['high'], row['low'], row['close'], row['volume']
#         ))

#     conn.commit()
#     cursor.close()
#     conn.close()
#     print("Data inserted successfully into PostgreSQL!")


