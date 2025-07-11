import streamlit as st
import pandas as pd
import requests

# --- LOAD DATA ---
@st.cache_data
def load_data():
    return pd.read_csv("data/cleaned_dataset.csv")

df = load_data()
# Convert release_date to datetime
df['release_date'] = pd.to_datetime(df['release_date'], format="%d/%m/%Y", errors='coerce')

# Extract year
df['release_year'] = df['release_date'].dt.year

# --- TITLE ---
st.title("🎬 Movie Finder")
st.markdown("Use filters to explore and discover movies!")

# --- SIDEBAR FILTERS ---
st.sidebar.header("🎛️ Filter Options")

# Genre, Language, Runtime (as before)
genres = st.sidebar.multiselect("🎭 Genre", df['genres'].dropna().unique())
language = st.sidebar.selectbox("🗣️ Language", df['original_language'].dropna().unique())
runtime_range = st.sidebar.slider("⏱️ Duration (min)", 0, 300, (60, 180))
df['release_date'] = pd.to_datetime(df['release_date'], format="%d/%m/%Y", errors='coerce')
df['release_year'] = df['release_date'].dt.year
min_year = int(df['release_year'].min())
max_year = int(df['release_year'].max())
year_range = st.sidebar.slider("📅 Release Year", min_year, max_year, (2000, 2023))
min_rating = st.sidebar.slider("⭐ Minimum Rating", 0.0, 10.0, 6.5)

# --- FILTERING LOGIC ---
filtered_df = df[
    df['genres'].str.contains('|'.join(genres), case=False, na=False) &
    (df['original_language'] == language) &
    (df['runtime'].between(runtime_range[0], runtime_range[1])) &
    (df['release_year'].between(year_range[0], year_range[1])) &
    (df['vote_average'] >= min_rating)
]


# --- SHOW MOVIE SUGGESTIONS ---
st.markdown(f"🎬 **Showing movies from {year_range[0]} to {year_range[1]}**, in _{language}_, rated at least **{min_rating}⭐**, between {runtime_range[0]} and {runtime_range[1]} minutes.")
st.subheader(f"🎯 {len(filtered_df)} movies found")
for _, row in filtered_df.head(20).iterrows():
    st.markdown(f"### {row['title']} ({int(row['release_year'])})")
    st.markdown(f"*{row['overview'][:300]}...*")
    st.markdown(f"**Genre**: {row['genres']} | **Language**: {row['original_language']} | **Runtime**: {row['runtime']} min")
    
    if st.button(f"Where to watch '{row['title']}'", key=row['title']):
        # OPTIONAL: Use real TMDb API here later
        st.info("🔄 Looking up streaming platforms...")
        st.success("📺 Available on: Netflix, Prime Video")  # Placeholder

    st.markdown("---")
