import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# st.title("🎮 VIDEO GAME SALES 1980 - 2016 🎮")
# st.subheader("Open the sidebar on the left 👈 to have a more control on the data")
# with st.sidebar:
#     st.title("")
#     range_of_year = st.slider(
#         "Select a range of year: ",
#         1980, 2016, (1980, 2016)
#     )
#     st.write(f"Currently showing data from {range_of_year[0]} to {range_of_year[1]}")


# @st.cache_data
# def load_data():
#     data = pd.read_csv("vgsales.csv")
#     data = data.dropna()
#     data['Year'] = data['Year'].to_datetime()
#     return data

# df = load_data()
# df

# Set page config
st.set_page_config(
    page_title="Video Game Sales Dashboard",
    page_icon="🎮",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("vgsales-clean.csv")  # Replace with your actual file path
    return df

# Load the data
df = load_data()

# Title
st.title("🎮 Video Game Sales Analysis Dashboard")

# Sidebar filters
st.sidebar.header("Filters")

# Year range slider
year_range = st.sidebar.slider(
    "Select Year Range",
    min_value=int(df['Year'].min()),
    max_value=int(df['Year'].max()),
    value=(int(df['Year'].min()), int(df['Year'].max()))
)

# Multi-select filters
selected_platforms = st.sidebar.multiselect(
    "Select Platforms",
    options=sorted(df['Platform'].unique()),
    default=[]
)

selected_genres = st.sidebar.multiselect(
    "Select Genres",
    options=sorted(df['Genre'].unique()),
    default=[]
)

selected_publishers = st.sidebar.multiselect(
    "Select Publishers",
    options=sorted(df['Publisher'].unique()),
    default=[]
)

# Filter the dataframe based on selections
filtered_df = df.copy()

if selected_platforms:
    filtered_df = filtered_df[filtered_df['Platform'].isin(selected_platforms)]
if selected_genres:
    filtered_df = filtered_df[filtered_df['Genre'].isin(selected_genres)]
if selected_publishers:
    filtered_df = filtered_df[filtered_df['Publisher'].isin(selected_publishers)]

filtered_df = filtered_df[
    (filtered_df['Year'] >= year_range[0]) &
    (filtered_df['Year'] <= year_range[1])
]

# Main content
# Row 1 - KPIs
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Games", len(filtered_df))
with col2:
    st.metric("Global Sales (M)", f"${filtered_df['Global_Sales'].sum():.2f}")
with col3:
    st.metric("Top Platform", filtered_df['Platform'].mode().iloc[0])
with col4:
    st.metric("Top Genre", filtered_df['Genre'].mode().iloc[0])

# Row 2 - Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sales by Region")
    sales_data = {
        'Region': ['North America', 'Europe', 'Japan', 'Other'],
        'Sales': [
            filtered_df['NA_Sales'].sum(),
            filtered_df['EU_Sales'].sum(),
            filtered_df['JP_Sales'].sum(),
            filtered_df['Other_Sales'].sum()
        ]
    }
    sales_df = pd.DataFrame(sales_data)
    fig = px.pie(sales_df, values='Sales', names='Region')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Top 10 Games by Global Sales")
    top_games = filtered_df.nlargest(10, 'Global_Sales')
    fig = px.bar(
        top_games,
        x='Name',
        y='Global_Sales',
        title='Top 10 Games by Global Sales'
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

# Row 3
st.subheader("Sales Trend Over Time")
yearly_sales = filtered_df.groupby('Year')[['Global_Sales']].sum().reset_index()
fig = px.line(
    yearly_sales,
    x='Year',
    y='Global_Sales',
    title='Global Sales Trend Over Time'
)
st.plotly_chart(fig, use_container_width=True)

# Data table
st.subheader("Raw Data")
st.dataframe(filtered_df)