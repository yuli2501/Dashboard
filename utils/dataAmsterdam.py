import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    df = pd.read_csv("Amsterdam.csv")
    df = df.drop(columns=["Unnamed: 0.1", "Unnamed: 0", "id", "scrape_id", "host_id"], errors="ignore")

    # ----------------- LIMPIEZA DE VARIABLES -----------------
    if 'host_acceptance_rate' in df.columns:
        df['host_acceptance_rate'] = df['host_acceptance_rate'].str.replace('%', '').astype(float) 

    if 'host_response_rate' in df.columns:
        df['host_response_rate'] = df['host_response_rate'].str.replace('%', '').astype(float) 

    # Eliminar espacios en los nombres de las columnas
    df.columns = df.columns.str.strip()

    numeric_df = df.select_dtypes(['float', 'int'])
    numeric_cols = numeric_df.columns
    text_df = df.select_dtypes(['object'])
    text_cols = text_df.columns
    unique_categories = df['host_is_superhost'].unique() if 'host_is_superhost' in df.columns else []

    return df, numeric_cols, text_cols, unique_categories, numeric_df

