import streamlit as st
import pandas as pd

# 🎬 Title of your app
st.title("🎬 Netflix Genre Finder")

# 🧠 Track if user wants to view visualization page
if "show_visual" not in st.session_state:
    st.session_state.show_visual = False

# 🧭 Toggle to visualization page
if st.button("📊 View Overall Visualization"):
    st.session_state.show_visual = True

# 📂 Load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles1.csv")
    return df

# 📈 Show visualization page
if st.session_state.show_visual:
    st.image("visualization.svg", caption="Genre Distribution Visualization", use_column_width=True)
    st.button("🔙 Back to Search", on_click=lambda: st.session_state.update(show_visual=False))

# 🔍 Otherwise, show the search interface
else:
    df = load_data()
    user_input = st.text_input("Type a movie or show title:")

    if user_input:
        matches = df[df['title'].str.lower().str.startswith(user_input.lower())]

        if not matches.empty:
            st.write(f"Found {len(matches)} result(s):")
            for _, row in matches.iterrows():
                title_with_year = f"{row['title']} ({int(row['release_year'])})"
                st.subheader(title_with_year)

                media_type = row.get('type', 'Unknown')
                rating = row.get('rating', 'Not Rated')
                st.markdown(
                    f"<span style='font-weight:bold;'>Type:</span> {media_type}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style='font-weight:bold;'>Rating:</span> {rating}",
                    unsafe_allow_html=True
                )

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
