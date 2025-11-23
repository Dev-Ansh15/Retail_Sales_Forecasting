import pandas as pd
import numpy as np
import os
import streamlit as st

def generate_mock_data(path):
    """Generates synthetic data if no file exists."""
    dates = pd.date_range(start='2021-01-01', end='2023-12-31', freq='D')
    data = []
    for _ in range(1000):
        date = np.random.choice(dates)
        sales = np.random.uniform(100, 5000)
        data.append([date, 'Store A', 'Product X', sales, 0.0])
    df = pd.DataFrame(data, columns=['Order Date', 'State', 'Sub-Category', 'Sales', 'Discount'])
    df.to_csv(path, index=False)
    return df

def load_data(file_path):
    """Loads data, maps columns, and performs feature engineering."""
    
    # 1. Generate mock if file missing
    if not os.path.exists(file_path):
        if 'uploaded' in file_path: return pd.DataFrame()
        generate_mock_data(file_path)

    # 2. Read CSV
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='latin1')

    # 3. Column Mapping
    col_map = {
        'Order Date': 'Date', 
        'Ship Date': 'Date_Ship',
        'State': 'Store', 
        'Region': 'Store_Region',
        'Sub-Category': 'Product',
        'Category': 'Product_Category',
        'Discount': 'Promo',
        'Sales': 'Sales'
    }
    df = df.rename(columns={k: v for k, v in col_map.items() if k in df.columns})
    
    # 4. Validation
    if 'Date' not in df.columns or 'Sales' not in df.columns:
        raise ValueError("CSV must contain 'Date' and 'Sales' columns.")

    # 5. Type Conversion
    df['Date'] = pd.to_datetime(df['Date'])
    df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce').fillna(0)
    
    # 6. Feature Engineering
    
    # FIX: Robust Promo handling
    if 'Promo' not in df.columns:
        df['Promo'] = 0.0
    else:
        df['Promo'] = pd.to_numeric(df['Promo'], errors='coerce').fillna(0.0)

    if 'Store' not in df.columns: df['Store'] = 'Default Store'
    if 'Product' not in df.columns: df['Product'] = 'General Item'

    df['Month'] = df['Date'].dt.month_name()
    df['DayOfWeek'] = df['Date'].dt.day_name()
    
    return df.sort_values('Date')