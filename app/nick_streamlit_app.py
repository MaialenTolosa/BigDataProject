from nick_api_utils import search_movies
import streamlit as st

st.set_page_config(layout="wide", page_title="Movie Explorer", page_icon="🎬")

st.title("🎬 Movie Explorer")

title = st.text_input("Enter a movie title")

if st.button("Search"):
    if title.strip() == "":
        st.warning("Please enter a movie title.")
    else:
        st.markdown(f"🔎 Searching for: **{title}**...")
        results = search_movies(title)

        if not results:
            st.error("❌ No results found.")
        else:
            st.success(f"✅ Found {len(results)} result(s).")

            # Sort by rating and votes descending
            sorted_results = sorted(
                results,
                key=lambda x: (
                    x.get("numVotes") or 0,     # Most votes first (popularity)
                    x.get("averageRating") or 0 # Then best rating
                ),
                reverse=True
            )


            for movie in sorted_results:
                title = movie.get('primaryTitle', 'Unknown')
                year = movie.get('startYear', 'N/A')
                st.markdown(f"### 🎬 {title} ({year})")

                # Image handling
                img_data = movie.get("primaryImage")
                img_url = None
                if isinstance(img_data, dict):
                    img_url = img_data.get("url")
                elif isinstance(img_data, str):
                    img_url = img_data

                col1, col2 = st.columns([1, 3])

                with col1:
                    if img_url:
                        st.image(img_url, width=220)

                with col2:
                    # Genres
                    genres_list = movie.get("genres")
                    genres = ", ".join(genres_list) if isinstance(genres_list, list) else "N/A"
                    st.markdown(f"**Genres:** {genres}")

                    # Rating and votes
                    rating = movie.get("averageRating", "N/A")
                    votes = movie.get("numVotes")
                    vote_text = f"{votes:,} votes" if isinstance(votes, int) else "No votes"
                    st.markdown(f"**Rating:** {rating} ⭐ ({vote_text})")

                    # Description
                    description = movie.get("description") or "No description available."
                    st.markdown(f"**Description:** {description}")

                    # IMDb Link
                    imdb_url = movie.get("url")
                    if imdb_url:
                        st.markdown(f"🔗 [IMDb Page]({imdb_url})")

                st.markdown("---")
