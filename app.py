import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Forest Area Dashboard")

# Load dataset
df = pd.read_csv("FAO_SDGB_24034_WIDEF.csv")

# Clean column names
df.columns = df.columns.str.strip()

# Keep ONLY needed columns
cols_to_keep = ["REF_AREA_LABEL", "2000", "2010", "2015", "2016", "2017", "2018", "2019", "2020"]
df = df[cols_to_keep]

# Convert to long format
df = df.melt(id_vars=["REF_AREA_LABEL"],
             var_name="Year",
             value_name="Value")

# Rename
df.rename(columns={"REF_AREA_LABEL": "Country"}, inplace=True)

# Remove missing values
df = df.dropna()