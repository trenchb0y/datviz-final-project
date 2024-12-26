import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Video Game Sales Dashboard - 1301213359",
    page_icon="📊",
    layout="wide"
)

def load_css(css_file):
    with open(css_file) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def apply_filters(df, platforms, genres, publishers, year_range):
    filtered_df = df.copy()
    
    if platforms:
        filtered_df = filtered_df[filtered_df['Platform'].isin(platforms)]
        if filtered_df.empty:
            return None, "No games found for the selected platform(s)"
            
    if genres:
        filtered_df = filtered_df[filtered_df['Genre'].isin(genres)]
        if filtered_df.empty:
            return None, "No games found for the selected genre(s)"
            
    if publishers:
        filtered_df = filtered_df[filtered_df['Publisher'].isin(publishers)]
        if filtered_df.empty:
            return None, "No games found for the selected publisher(s)"
    
    filtered_df = filtered_df[
        (filtered_df['Year'] >= year_range[0]) &
        (filtered_df['Year'] <= year_range[1])
    ]
    if filtered_df.empty:
        return None, "No games found in the selected year range"
    
    return filtered_df, None

@st.cache_data
def load_data():
    df = pd.read_csv("vgsales-clean.csv")
    return df

load_css('style.css')

df = load_data()

st.title("🎮📊 Video Game Sales Analysis Dashboard")
st.write("Open the sidebar on the left 👈 for an addtional control on the data")

st.sidebar.header("Filters")

year_range = st.sidebar.slider(
    "Select Year Range",
    min_value=int(df['Year'].min()),
    max_value=int(df['Year'].max()),
    value=(int(df['Year'].min()), int(df['Year'].max()))
)

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

# filtered_df = df.copy()

filtered_df, error_message = apply_filters(
    df, 
    selected_platforms, 
    selected_genres, 
    selected_publishers, 
    year_range
)

if error_message:
    st.error(error_message)
    st.stop()
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

st.markdown("### Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Games", len(filtered_df))
with col2:
    st.metric("Global Sales (M)", f"${filtered_df['Global_Sales'].sum():.2f}")
with col3:
    platform_mode = filtered_df['Platform'].mode()
    top_platform = platform_mode.iloc[0] if not platform_mode.empty else "N/A"
    st.metric("Top Platform", top_platform)
with col4:
    genre_mode = filtered_df['Genre'].mode()
    top_genre = genre_mode.iloc[0] if not genre_mode.empty else "N/A"
    st.metric("Top Genre", top_genre)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Sales by Region")
    if filtered_df['Global_Sales'].sum() > 0:
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
    else:
        st.info("No sales data available for the selected filters")

with col2:
    st.subheader("Top 10 Games by Global Sales")
    if not filtered_df.empty:
        top_games = filtered_df.nlargest(min(10, len(filtered_df)), 'Global_Sales')
        fig = px.bar(
            top_games,
            x='Name',
            y='Global_Sales',
            title=f"Top {len(top_games)} Games by Global Sales"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No games data available for the selected filters")

st.subheader("Sales Trend Over Time")
if not filtered_df.empty:
    yearly_sales = filtered_df.groupby('Year')[['Global_Sales']].sum().reset_index()
    if len(yearly_sales) > 0:
        fig = px.line(
            yearly_sales,
            x='Year',
            y='Global_Sales',
            title='Global Sales Trend Over Time'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No trend data available for the selected filters")
else:
    st.info("No trend data available for the selected filters")

st.subheader("Raw Data")
if not filtered_df.empty:
    st.dataframe(filtered_df)
else:
    st.info("No data available for the selected filters")

st.write("Made with 🫀 by yours truly -zharfan.")