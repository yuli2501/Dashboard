import pandas as pd
import streamlit as st

@st.cache_data
def load_dataMilan():
    df = pd.read_csv("Milan.csv")
    df = df.drop(columns=["id", "host_id"], errors="ignore")

    numericMilan = df.select_dtypes(['float', 'int'])
    numeric_colsMilan = numericMilan.columns
    textMilan = df.select_dtypes(['object'])
    text_colsMilan = textMilan.columns
    unique_categoriesMilan = df['host_is_superhost'].unique() if 'host_is_superhost' in df.columns else []

    return df, numeric_colsMilan, text_colsMilan, unique_categoriesMilan, numericMilan