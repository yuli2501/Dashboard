import pandas as pd
import streamlit as st

@st.cache_data
def load_dataHongKong():
    df = pd.read_csv("HongKong.csv")
    df = df.drop(columns=["Unnamed: 0", "id", "scrape_id", "host_id"], errors="ignore")

    numericHongKong = df.select_dtypes(['float', 'int'])
    numeric_colsHongKong = numericHongKong.columns
    textHongKong = df.select_dtypes(['object'])
    text_colsHongKong = textHongKong.columns
    unique_categoriesHongKong = df['host_is_superhost'].unique() if 'host_is_superhost' in df.columns else []

    return df, numeric_colsHongKong, text_colsHongKong, unique_categoriesHongKong, numericHongKong