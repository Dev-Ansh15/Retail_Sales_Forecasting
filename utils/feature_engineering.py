import pandas as pd

def create_time_features(df):
    df = df.copy()
    df['Date'] = pd.to_datetime(df['Date'])
    df['DayOfWeek'] = df['Date'].dt.dayofweek
    df['Month'] = df['Date'].dt.month
    df['Year'] = df['Date'].dt.year
    df['DayOfYear'] = df['Date'].dt.dayofyear
    df['IsWeekend'] = (df['DayOfWeek'] >= 5).astype(int)
    return df

def create_lag_features(df, lags=[1, 7, 30]):
    df = df.copy()
    for lag in lags:
        df[f'Sales_Lag_{lag}'] = df['Sales'].shift(lag)
    return df.dropna()