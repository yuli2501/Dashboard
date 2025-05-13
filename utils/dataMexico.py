import pandas as pd
import streamlit as st

@st.cache_data
def load_dataMexico():
    df = pd.read_csv("Mexico.csv")
    df = df.drop(columns=["id", "host_id"], errors="ignore")

    numericMexico = df.select_dtypes(['float', 'int'])
    numeric_colsMex = numericMexico.columns
    textMexico = df.select_dtypes(['object'])
    text_colsMex = textMexico.columns
    unique_categoriesMex = df['host_is_superhost'].unique() if 'host_is_superhost' in df.columns else []

    return df, numeric_colsMex, text_colsMex, unique_categoriesMex, numericMexico