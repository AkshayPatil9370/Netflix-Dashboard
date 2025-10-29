import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from collections import Counter

# Set page configuration
st.set_page_config(
    page_title="Netflix Content Analysis Dashboard",
    page_icon="🎬",
    layout="wide")

# Title and description
st.title("🎬 Netflix Content Analysis Dashboard")
st.markdown("An interactive analysis of Netflix's content library")


# Load and preprocess the data
@st.cache_data
def load_data():
    df = pd.read_csv('netflix_titles.csv')

    # Convert date columns
    df['date_added'] = pd.to_datetime(df['date_added'])
    df['release_year'] = pd.to_datetime(df['release_year'].astype(str), format='%Y')

    # Remove entries with unspecified director and cast
    df = df.dropna(subset=['director', 'cast'])

    # Extract numeric duration
    df['duration_num'] = df['duration'].str.extract(r'(\d+)').astype(float)
    df['duration_unit'] = df['duration'].str.extract(r'(\D+)').fillna('')

    # Create month-year column for trend analysis
    df['month_added'] = df['date_added'].dt.to_period('M')

    return df


df = load_data()

# Create tabs for better organization
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Main Metrics",
    "📈 Trends & Patterns",
    "🔍 Content Analysis",
    "👥 Cast & Crew",
    "🗺 Country / Year / Month Explorer"
])

# Sidebar filters
st.sidebar.header("Filters")

# Type filter (Movie/TV Show)
type_filter = st.sidebar.multiselect(
    "Select Content Type",
    options=df['type'].unique(),
    default=df['type'].unique()
)

# Year range filter
min_year = int(df['release_year'].dt.year.min())
max_year = int(df['release_year'].dt.year.max())
year_range = st.sidebar.slider(
    "Release Year Range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# Filter the dataframe
filtered_df = df[
    (df['type'].isin(type_filter)) &
    (df['release_year'].dt.year.between(year_range[0], year_range[1]))
]

# Tab 1: Main Metrics
with tab1:
    col1, col2 = st.columns(2)

    # Content Type Distribution
    with col1:
        st.subheader("Content Type Distribution")
        fig_type = px.pie(
            filtered_df,
            names='type',
            title='Distribution of Movies and TV Shows',
            hole=0.4
        )
        st.plotly_chart(fig_type, use_container_width=True, key="fig_type")

    # Rating Distribution
    with col2:
        st.subheader("Rating Distribution")
        rating_counts = filtered_df['rating'].value_counts()
        fig_rating = px.pie(
            values=rating_counts.values,
            names=rating_counts.index,
            title='Content Ratings Distribution',
            hole=0.4
        )
        st.plotly_chart(fig_rating, use_container_width=True, key="fig_rating")

    # Duration Analysis
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Duration Analysis")
        # Separate movies and TV shows
        movies_duration = filtered_df[filtered_df['type'] == 'Movie']['duration_num']
        tv_duration = filtered_df[filtered_df['type'] == 'TV Show']['duration_num']

        fig_duration = go.Figure()
        fig_duration.add_trace(go.Box(y=movies_duration, name='Movies', boxpoints='outliers'))
        fig_duration.add_trace(go.Box(y=tv_duration, name='TV Shows', boxpoints='outliers'))
        fig_duration.update_layout(title='Duration Distribution by Content Type',
                                 yaxis_title='Duration')
        st.plotly_chart(fig_duration, use_container_width=True, key="fig_duration")

    with col4:
        st.subheader("Top 10 Genres")
        genres = filtered_df['listed_in'].str.split(',', expand=True).stack()
        genre_counts = genres.value_counts().head(10)
        fig_genres = px.bar(
            x=genre_counts.values,
            y=genre_counts.index,
            orientation='h',
            title='Top 10 Genres',
            labels={'x': 'Count', 'y': 'Genre'}
        )
        st.plotly_chart(fig_genres, use_container_width=True, key="fig_genres")

# Tab 2: Trends & Patterns
with tab2:
    col1, col2 = st.columns(2)

    # Release Year Trend
    with col1:
        st.subheader("Content Release Trend")
        yearly_counts = filtered_df.groupby(filtered_df['release_year'].dt.year).size().reset_index()
        yearly_counts.columns = ['year', 'count']
        fig_trend = px.line(
            yearly_counts,
            x='year',
            y='count',
            title='Content Added Over Years'
        )
        st.plotly_chart(fig_trend, use_container_width=True, key="fig_trend")

    # Monthly Addition Pattern
    with col2:
        st.subheader("Monthly Addition Pattern")
        monthly_adds = filtered_df.groupby(filtered_df['date_added'].dt.month).size()
        fig_monthly = px.bar(
            x=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            y=monthly_adds.values if len(monthly_adds) > 0 else [0]*12,
            title='Content Added by Month',
            labels={'x': 'Month', 'y': 'Number of Titles'}
        )
        st.plotly_chart(fig_monthly, use_container_width=True, key="fig_monthly_main")

    # Genre Trends Over Time
    st.subheader("Genre Trends Over Time")
    # Build a per-year counter of listed_in values safely (handle NaNs)
    genres_by_year = (
        filtered_df[filtered_df['listed_in'].notna()]
        .groupby(filtered_df['release_year'].dt.year)['listed_in']
        .agg(lambda x: Counter(', '.join(x).split(', ')))
        .reset_index()
    )
    top_genres = filtered_df['listed_in'].str.split(', ', expand=True).stack().value_counts().head(5).index

    genre_trend_data = []
    for year in genres_by_year['release_year']:
        year_counts = genres_by_year[genres_by_year['release_year'] == year]['listed_in'].iloc[0]
        for genre in top_genres:
            genre_trend_data.append({
                'year': year,
                'genre': genre,
                'count': year_counts[genre] if genre in year_counts else 0
            })

    genre_trend_df = pd.DataFrame(genre_trend_data)
    fig_genre_trends = px.line(
        genre_trend_df,
        x='year',
        y='count',
        color='genre',
        title='Top 5 Genre Trends Over Time',
        labels={'count': 'Number of Titles', 'year': 'Year'}
    )
    st.plotly_chart(fig_genre_trends, use_container_width=True, key="fig_genre_trends_tab2")

# Tab 3: Content Analysis
with tab3:
    # Content by Country
    st.subheader("Content by Country")
    country_counts = filtered_df['country'].value_counts().head(15)
    fig_countries = px.bar(
        x=country_counts.index,
        y=country_counts.values,
        title='Top 15 Countries by Content Production',
        labels={'x': 'Country', 'y': 'Number of Titles'}
    )
    st.plotly_chart(fig_countries, use_container_width=True, key="fig_countries")

    # Rating vs Duration Analysis
    st.subheader("Rating vs Duration Analysis")
    fig_rating_duration = px.box(
        filtered_df[filtered_df['type'] == 'Movie'],
        x='rating',
        y='duration_num',
        title='Movie Duration by Rating',
        labels={'duration_num': 'Duration (minutes)', 'rating': 'Rating'}
    )
    st.plotly_chart(fig_rating_duration, use_container_width=True, key="fig_rating_duration")

    # Content Release Heatmap
    st.subheader("Content Release Heatmap")
    release_heatmap = filtered_df.groupby([filtered_df['date_added'].dt.year, filtered_df['date_added'].dt.month]).size().unstack()
    fig_heatmap = px.imshow(
        release_heatmap,
        labels=dict(x="Month", y="Year", color="Number of Releases"),
        aspect="auto",
        title="Content Release Heatmap"
    )
    st.plotly_chart(fig_heatmap, use_container_width=True, key="fig_heatmap")

# Tab 4: Cast & Crew Analysis
with tab4:
    col1, col2 = st.columns(2)

    with col1:
        # Top Directors Analysis
        st.subheader("Top Directors")
        # Clean and process director data
        directors_df = filtered_df[filtered_df['director'].notna()]  # Remove rows with NaN directors
        directors_df = directors_df[~directors_df['director'].str.contains('Not Specified', case=False, na=False)]  # Remove Not Specified

        directors = (directors_df['director']
                    .str.split(',', expand=True)
                    .stack()
                    .str.strip()
                    .replace('', pd.NA)
                    .dropna())

        director_counts = directors.value_counts().head(10)

        fig_directors = px.bar(
            x=director_counts.values,
            y=director_counts.index,
            orientation='h',
            title='Top 10 Directors by Number of Titles',
            labels={'x': 'Number of Titles', 'y': 'Director'}
        )
        st.plotly_chart(fig_directors, use_container_width=True, key="fig_directors")

    with col2:
        # Top Actors Analysis
        st.subheader("Top Actors")
        # Clean and process cast data
        cast_df = filtered_df[filtered_df['cast'].notna()]  # Remove rows with NaN cast
        cast_df = cast_df[~cast_df['cast'].str.contains('Not Specified', case=False, na=False)]  # Remove Not Specified

        actors = (cast_df['cast']
                 .str.split(',', expand=True)
                 .stack()
                 .str.strip()
                 .replace('', pd.NA)
                 .dropna())

        actor_counts = actors.value_counts().head(10)

        fig_actors = px.bar(
            x=actor_counts.values,
            y=actor_counts.index,
            orientation='h',
            title='Top 10 Actors by Number of Appearances',
            labels={'x': 'Number of Appearances', 'y': 'Actor'}
        )
        st.plotly_chart(fig_actors, use_container_width=True, key="fig_actors")

    # Director-Genre Network
    st.subheader("Director's Genre Preferences")
    director_genre_data = []

    # Filter out rows with 'Not Specified' directors first
    valid_content = filtered_df[
        (filtered_df['director'].notna()) & 
        (~filtered_df['director'].str.contains('Not Specified', case=False, na=False)) &
        (filtered_df['listed_in'].notna())
    ]

    for _, row in valid_content.iterrows():
        directors = [d.strip() for d in row['director'].split(',') if d.strip()]
        genres = [g.strip() for g in row['listed_in'].split(',') if g.strip()]

        for director in directors:
            for genre in genres:
                director_genre_data.append({
                    'Director': director,
                    'Genre': genre
                })

    director_genre_df = pd.DataFrame(director_genre_data)
    top_directors = director_genre_df['Director'].value_counts().head(5).index

    director_genre_pivot = pd.crosstab(
        director_genre_df[director_genre_df['Director'].isin(top_directors)]['Director'],
        director_genre_df[director_genre_df['Director'].isin(top_directors)]['Genre']
    )

    fig_director_genre = px.imshow(
        director_genre_pivot,
        title="Top Directors' Genre Preferences",
        labels=dict(x="Genre", y="Director", color="Number of Titles")
    )
    st.plotly_chart(fig_director_genre, use_container_width=True, key="fig_director_genre")




# Country / Year / Month Explorer (tab5)
with tab5:
    st.title("Country / Year / Month Explorer")
    st.write("Select a year and month to see the number of titles posted by country.")

    # Year and month selectors derived from `date_added` in the full dataset
    available_years = sorted(df['date_added'].dt.year.dropna().astype(int).unique())
    year_options = ['All'] + available_years
    sel_year = st.selectbox("Select Year", options=year_options, index=len(year_options)-1)

    month_names = ['All', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    sel_month = st.selectbox("Select Month", options=month_names, index=0)

    # Country selector (default to top 10 countries in full dataset)
    countries_all = (df['country'].dropna()
                     .str.split(',')
                     .explode()
                     .str.strip())
    top_countries = countries_all.value_counts().head(20).index.tolist()
    sel_countries = st.multiselect("Select Countries (optional)", options=top_countries, default=top_countries[:10])

    # Build subset from full dataset `df` based on selections
    subset = df.dropna(subset=['date_added']).copy()
    if sel_year != 'All':
        subset = subset[subset['date_added'].dt.year == int(sel_year)]
    if sel_month != 'All':
        month_idx = month_names.index(sel_month)
        subset = subset[subset['date_added'].dt.month == month_idx]

    # Explode countries and filter
    countries_exploded = subset.dropna(subset=['country']).assign(
        country=subset['country'].str.split(',')).explode('country')
    countries_exploded['country'] = countries_exploded['country'].str.strip()

    if sel_countries:
        countries_exploded = countries_exploded[countries_exploded['country'].isin(sel_countries)]

    # Aggregate counts by country
    country_counts = (
        countries_exploded['country']
        .value_counts()
        .reset_index()
    )
    country_counts.columns = ['country', 'count']

    st.subheader("Titles Posted by Country")
    if country_counts.empty:
        st.info("No content found for the selected year/month/country filters.")
    else:
        fig_country_counts = px.bar(country_counts, x='country', y='count', title='Titles Posted by Country', labels={'count': 'Number of Titles', 'country': 'Country'})
        st.plotly_chart(fig_country_counts, use_container_width=True, key="fig_country_counts")
        st.dataframe(country_counts)



# Detailed Content Listing
st.subheader("Content Details")
if st.checkbox("Show Content Details"):
    st.dataframe(
        filtered_df[['title', 'type', 'release_year', 'duration', 'rating']]
        .sort_values('release_year', ascending=False)
    )

# Show raw data
if st.checkbox("Show Raw Data"):
    st.subheader("Raw Data")
    st.write(filtered_df)