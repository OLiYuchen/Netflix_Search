import streamlit as st
import pandas as pd

# 🎬 Title of your app
st.title("🎬 Netflix Genre Finder")

# 📂 Load the dataset (with caching to speed things up)
@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles1.csv")
    return df

df = load_data()

# 🔎 Text input for searching
user_input = st.text_input("Type a movie or show title:")

# 🔍 Filter matching titles
if user_input:
    matches = df[df['title'].str.lower().str.startswith(user_input.lower())]

    if not matches.empty:
        st.write(f"Found {len(matches)} result(s):")
        for _, row in matches.iterrows():
            st.subheader(row['title'])

            st.markdown(f"**Year:** {row['release_year']}")

            # Get available genres
            genres = [
                row.get('Genre split 1', ''),
                row.get('Genre split 2', ''),
                row.get('Genre split 3', '')
            ]
            genres = [g for g in genres if pd.notna(g) and g != '']
            
            st.markdown(f"**Genres:** {', '.join(genres)}")
            st.markdown(f"**Description:** {row['description']}")
            st.markdown("---")
    else:
        st.warning("No matching titles found.")
