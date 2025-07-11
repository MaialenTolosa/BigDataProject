from nick_api_utils import search_movies
import streamlit as st

st.set_page_config(layout="wide", page_title="Movie Explorer", page_icon="🎬")

st.title("🎬 Movie Explorer")

title = st.text_input("Enter a movie title")

from nick_api_utils import search_movies, get_watchmode_id_by_imdb, get_streaming_sources

if st.button("Search"):
    if title.strip() == "":
        st.warning("Please enter a movie title.")
    else:
        st.markdown(f"🔎 Searching for: **{title}**...")
        with st.spinner("Searching..."):
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
                movie_title = movie.get('primaryTitle', 'Unknown')
                year = movie.get('startYear', 'N/A')
                st.markdown(f"### 🎬 {movie_title} ({year})")

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

                    
                    # Watchmode Integration
                    watchmode_id = get_watchmode_id_by_imdb(movie.get("id"))
                    if watchmode_id:
                        sources = get_streaming_sources(watchmode_id)
                        if sources:
                        # Filter subscription sources only
                            sub_sources = [s for s in sources if s.get("type") == "sub"]
                            if sub_sources:
                                st.markdown("📺 **Available on:**")

                                # Known platform logos
                                platform_logos = {
                                    "Netflix": "https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg",
                                    "Amazon Prime": "https://upload.wikimedia.org/wikipedia/commons/f/f1/Prime_Video.png",
                                    "Disney+": "https://upload.wikimedia.org/wikipedia/commons/3/3e/Disney%2B_logo.svg",
                                    "HBO Max": "https://upload.wikimedia.org/wikipedia/commons/1/17/HBO_Max_Logo.svg",
                                    "Apple TV+": "https://upload.wikimedia.org/wikipedia/commons/1/1b/Apple_TV_Plus_Logo.svg",
                                    "Paramount Plus": "https://upload.wikimedia.org/wikipedia/commons/b/bc/Paramount%2B_logo.svg"
                                }

                                # Deduplicate by platform name
                                unique_platforms = {}
                                for s in sub_sources:
                                    name = s.get("name")
                                    if name not in unique_platforms:
                                        unique_platforms[name] = platform_logos.get(name)

                                # Display in a neat grid
                                cols = st.columns(min(len(unique_platforms), 5))  # Adjust grid size as needed

                                for i, (name, logo) in enumerate(unique_platforms.items()):
                                    with cols[i % len(cols)]:
                                        if logo:
                                            st.image(logo, width=80)
                                        else:
                                            st.markdown(f"- {name}")



                st.markdown("---")

