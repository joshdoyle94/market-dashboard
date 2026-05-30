import pandas as pd
import math

def calculate_daily_returns(df):
    return df["Close"].pct_change()

def calculate_moving_average(df, window):
    return df["Close"].rolling(window=window).mean()

def calculate_volatility(df, window):
    daily_rts = df["Close"].pct_change()
    
    rolling_std = daily_rts.rolling(window=window).std()
    
    annualized_volatility = rolling_std * math.sqrt(252)
    
    return annualized_volatility

def calculate_all(df):
    windows = [20, 50]
    results = {}
    daily = calculate_daily_returns(df)

    for window in windows:
        moving_avg = calculate_moving_average(df, window)
        vol = calculate_volatility(df, window)

        results[window] = {
            "daily_returns": daily,
            "moving_average": moving_avg,
            "volatility": vol
        }
        
    return results