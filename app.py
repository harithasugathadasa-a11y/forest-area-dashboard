import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Forest Area Dashboard")

df = pd.read_csv("FAO_SDGB_24034_WIDEF.csv")


df.columns = df.columns.str.strip()

cols_to_keep = ["REF_AREA_LABEL", "2000", "2010", "2015", "2016", "2017", "2018", "2019", "2020"]
df = df[cols_to_keep]

df = df.melt(id_vars=["REF_AREA_LABEL"],
             var_name="Year",
             value_name="Value")


df.rename(columns={"REF_AREA_LABEL": "Country"}, inplace=True)

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


# Dropdown
country = st.selectbox("Select Country", df["Country"].unique())

# Filter
filtered_df = df[df["Country"] == country]

# Show data
st.write(filtered_df)

# Chart
st.line_chart(filtered_df.set_index("Year")["Value"])



# This chart shows the change in forest area (percentage of land)
# between 2000 and 2020 for each country.
# Values represent percentage point changes.

st.subheader("Change from 2000 to 2020")

df_2000 = df[df["Year"] == "2000"][["Country", "Value"]]
df_2020 = df[df["Year"] == "2020"][["Country", "Value"]]

change_df = df_2000.merge(df_2020, on="Country", suffixes=("_2000", "_2020"))

change_df["Change"] = change_df["Value_2020"] - change_df["Value_2000"]

# Top increases
top_change = change_df.sort_values(by="Change", ascending=False).head(10)

st.bar_chart(top_change.set_index("Country")["Change"])



#Shows the global pattern, not just one country
st.subheader("Average Forest Area Trend (All Countries)")

avg_trend = df.groupby("Year")["Value"].mean()

st.line_chart(avg_trend)



#Most Decreased country (Forest Area )

st.subheader("Top 10 Decreases in Forest Area (2000–2020)")

bottom_change = change_df.sort_values(by="Change", ascending=True).head(10)

st.bar_chart(bottom_change.set_index("Country")["Change"])



#Most Increased country (Forest Area )
st.subheader("Top 10 Increases in Forest Area (2000–2020)")

top_change = change_df.sort_values(by="Change", ascending=False).head(10)

st.bar_chart(top_change.set_index("Country")["Change"])





#To shows how forest area percentages change across countries over different years using colors.
st.subheader("Heatmap: Forest Area by Country and Year")

# Choose countries
selected_countries = st.multiselect(
    "Select Countries",
    df["Country"].unique(),
    default=df["Country"].unique()[:10]
)

# Filter selected countries
heatmap_df = df[df["Country"].isin(selected_countries)]


heatmap_data = heatmap_df.pivot_table(
    index="Country",
    columns="Year",
    values="Value"
)

fig = px.imshow(
    heatmap_data,
    labels=dict(x="Year", y="Country", color="Forest Area %"),
    aspect="auto",
    color_continuous_scale="Reds",
    title="Forest Area Heatmap"
)

st.plotly_chart(fig, use_container_width=True)






# Shows how forest area percentages are distributed across all countries for each year using a box plot.
# Helps identify median values, spread, and overall variation between countries.
st.subheader("Global Distribution of Forest Area by Year")

fig = px.box(
    df,
    x="Year",
    y="Value",
    points="outliers",
    color="Year",
    title="Forest Area Distribution Across Countries"
)

st.plotly_chart(fig, use_container_width=True)