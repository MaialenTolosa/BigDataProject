import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://imdb236.p.rapidapi.com/api/imdb/search"

HEADERS = {"Authorization": f"Bearer {API_KEY}"}

st.set_page_config(page_title="TMDb Movie Finder", layout="wide")
st.title("🎬 TMDb Movie Explorer")

# --- GENRE OPTIONS ---
@st.cache_data
def get_genres():
    res = requests.get(f"{BASE_URL}/genre/movie/list", headers=HEADERS)
    return res.json().get("genres", [])

genres = get_genres()
genre_dict = {g['name']: g['id'] for g in genres}
genre_names = list(genre_dict.keys())

# --- USER INPUT ---
st.sidebar.header("🔍 Filter Options")
query = st.sidebar.text_input("🔎 Search movie title")
selected_genres = st.sidebar.multiselect("🎭 Genre", genre_names)
year = st.sidebar.slider("📅 Release Year", 1950, 2025, 2020)

# --- SEARCH FUNCTION ---
def search_movies(title="", genre_ids=[], year=None):
    url = f"{BASE_URL}/search/movie" if title else f"{BASE_URL}/discover/movie"
    params = {
        "query": title,
        "with_genres": ",".join(map(str, genre_ids)) if genre_ids else None,
        "primary_release_year": year if year else None,
        "sort_by": "popularity.desc"
    }
    res = requests.get(url, headers=HEADERS, params=params)
    return res.json().get("results", [])

# --- STREAMING INFO ---
def get_watch_providers(movie_id):
    res = requests.get(f"{BASE_URL}/movie/{movie_id}/watch/providers", headers=HEADERS)
    return res.json().get("results", {}).get("DE", {}).get("flatrate", [])  # Change 'DE' for your country

# --- FETCH & DISPLAY ---
genre_ids = [genre_dict[g] for g in selected_genres]
results = search_movies(query, genre_ids, year)

st.subheader(f"🎯 Found {len(results)} movies")
for movie in results[:20]:
    st.markdown(f"### {movie['title']} ({movie.get('release_date', 'N/A')[:4]})")
    st.markdown(f"*{movie.get('overview', 'No description available')[:300]}...*")

    # Streaming Info
    providers = get_watch_providers(movie["id"])
    if providers:
        st.success("📺 Available on: " + ", ".join([p["provider_name"] for p in providers]))
    else:
        st.warning("No streaming info found.")

    st.markdown("---")
