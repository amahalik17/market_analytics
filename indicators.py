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
    df['RSI'] = (100 - (100 / (1 + rs))).round(0)

    return df



# Rsi_divergence function to output detailed DataFrame
def rsi_divergence(df, ticker, period=14, column='close'):
    if not isinstance(period, int) or period <= 0:
        raise ValueError("The 'period' parameter must be an integer greater than 0.")
    # Calculate RSI
    df = calculate_rsi(df, period, column)

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



# Fibonacci retracement levels in percentages
fib_levels = [0.236, 0.382, 0.5, 0.618, 0.786]

def fib_retracement(df, column='close'):
    # Find the recent high and low within the DataFrame
    high = df[column].max()
    low = df[column].min()

    # Calculate Fibonacci retracement levels
    fib_levels = {}
    for level in fib_levels:
        retracement_level = high - (high - low) * level
        fib_levels[f"Level_{int(level*100)}%"] = retracement_level

    # Add the high and low for reference
    fib_levels["High"] = high
    fib_levels["Low"] = low

    # Create a DataFrame for displaying the levels
    fib_df = pd.DataFrame(fib_levels, index=[0])
    return fib_df



# TTM Squeeze Indicator
def ttm_squeeze(df, period=20, stddev_multiplier=2, atr_multiplier=1.5, column='close'):
    # Calculate Bollinger Bands
    df['SMA'] = df[column].rolling(window=period).mean()
    df['Bollinger_Upper'] = df['SMA'] + stddev_multiplier * df[column].rolling(window=period).std()
    df['Bollinger_Lower'] = df['SMA'] - stddev_multiplier * df[column].rolling(window=period).std()

    # Calculate Keltner Channels
    df['ATR'] = df['high'].rolling(window=period).max() - df['low'].rolling(window=period).min()
    df['Keltner_Upper'] = df['SMA'] + atr_multiplier * df['ATR']
    df['Keltner_Lower'] = df['SMA'] - atr_multiplier * df['ATR']

    # Determine squeeze
    df['Squeeze_On'] = (df['Bollinger_Lower'] > df['Keltner_Lower']) & (df['Bollinger_Upper'] < df['Keltner_Upper'])
    df['Squeeze_Off'] = (df['Bollinger_Lower'] <= df['Keltner_Lower']) | (df['Bollinger_Upper'] >= df['Keltner_Upper'])

    # Calculate momentum using a simple rate of change or RSI for direction
    df['Momentum'] = (df[column] - df[column].shift(period)).fillna(0)

    # Clean up DataFrame to show only necessary columns
    result = df[['date', column, 'Bollinger_Upper', 'Bollinger_Lower', 'Keltner_Upper', 'Keltner_Lower', 'Squeeze_On', 'Squeeze_Off', 'Momentum']]

    return result


