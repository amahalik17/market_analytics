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
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

