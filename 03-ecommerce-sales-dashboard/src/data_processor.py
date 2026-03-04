
# Data Processor
# Prajwal Kondala | IIT Kharagpur

import pandas as pd
import numpy as np

def load_data(filepath):
    """Load raw data from CSV"""
    df = pd.read_csv(filepath, encoding='latin-1')
    return df

def clean_data(df):
    """Clean and prepare data"""
    df = df[~df['Invoice'].astype(str).str.startswith('C')]
    df = df[df['Quantity'] > 0]
    df = df[df['Price'] > 0]
    df = df.dropna(subset=['Description'])
    df['Customer ID'] = df['Customer ID'].fillna(0).astype(int)
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['Revenue'] = df['Quantity'] * df['Price']
    return df

def engineer_features(df):
    """Add derived features"""
    df['Year'] = df['InvoiceDate'].dt.year
    df['Month'] = df['InvoiceDate'].dt.month
    df['DayName'] = df['InvoiceDate'].dt.day_name()
    df['YearMonth'] = df['InvoiceDate'].dt.to_period('M')
    return df

def split_dataframes(df):
    """Split into sales and customer DataFrames"""
    sales_df = df[['Invoice', 'StockCode', 'Description',
                   'Quantity', 'InvoiceDate', 'Price',
                   'Revenue', 'Year', 'Month', 'DayName', 'YearMonth']].copy()
    customer_df = df[['Customer ID', 'Country']].drop_duplicates().copy()
    customer_df = customer_df[customer_df['Customer ID'] != 0]
    return sales_df, customer_df

def segment_customer(revenue):
    """Segment customers by revenue"""
    if revenue >= 5000: return 'High Value'
    elif revenue >= 1000: return 'Medium Value'
    else: return 'Low Value'
