# Import dependencies
import pandas as pd
import numpy as np


# RSI (Relative Strength Index)
def calculate_rsi(df, period=14, column='close'):

    # Calculate the difference in price from the previous day
    delta = df[column].diff()
    
    # Get the gain and loss
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    # Calculate the RSI
    rs = gain / loss
    rsi = (100 - (100 / (1 + rs))).round(0)

    return rsi


# Rsi_divergence function to output detailed DataFrame
def rsi_divergence(df, ticker, period=14, column='close'):
    if not isinstance(period, int) or period <= 0:
        raise ValueError("The 'period' parameter must be an integer greater than 0.")
    # Calculate RSI
    df['RSI'] = calculate_rsi(df, ticker, period, column)['RSI']

    # Initialize columns for divergence types
    df['Bullish_Divergence'] = False
    df['Bearish_Divergence'] = False

    # Loop through each RSI value to check for divergence
    for i in range(period, len(df) - 1):
        # Current RSI and close price
        current_rsi = df['RSI'].iloc[i]
        current_close = df[column].iloc[i]

        # Previous RSI and close price for comparison
        prev_rsi = df['RSI'].iloc[i - 1]
        prev_close = df[column].iloc[i - 1]

        # Check for bullish divergence (RSI increasing, price decreasing)
        if current_rsi > prev_rsi and current_close < prev_close:
            df.at[i, 'Bullish_Divergence'] = True
        # Check for bearish divergence (RSI decreasing, price increasing)
        elif current_rsi < prev_rsi and current_close > prev_close:
            df.at[i, 'Bearish_Divergence'] = True

    # Filter only the rows with detected divergences
    divergence_df = df.loc[df['Bullish_Divergence'] | df['Bearish_Divergence'], ['date', 'RSI', 'Bullish_Divergence', 'Bearish_Divergence']]
    divergence_df['Ticker'] = ticker

    # Reorder columns
    divergence_df = divergence_df[['Ticker', 'date', 'RSI', 'Bullish_Divergence', 'Bearish_Divergence']]

    return divergence_df

