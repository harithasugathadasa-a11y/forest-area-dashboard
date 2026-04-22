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



# Year dropdown
year_selected = st.selectbox("Select Year", sorted(df["Year"].unique()))

# Filter data
year_data = df[df["Year"] == year_selected]

st.subheader(f"Top 10 Countries by Forest Area (%) in {year_selected}")

top10 = year_data.sort_values(by="Value", ascending=False).head(10)

st.bar_chart(top10.set_index("Country")["Value"])



st.subheader("Country Comparison")

year_selected = st.selectbox("Select Year for Comparison", df["Year"].unique())

year_data = df[df["Year"] == year_selected]

year_data = year_data.sort_values(by="Value", ascending=False)

fig = px.bar(
    year_data.head(30),
    x="Value",
    y="Country",
    orientation="h",
    title=f"Country Comparison - {year_selected}",
    height=1200
)

st.plotly_chart(fig, use_container_width=True)