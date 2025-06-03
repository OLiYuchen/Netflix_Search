import streamlit as st
import pandas as pd
from pathlib import Path

# Set custom page width with CSS
st.markdown(
    """
    <style>
        /* Widen main content */
        .block-container {
            padding-left: 4rem;
            padding-right: 4rem;
            max-width: 1200px;
        }

        /* Sidebar button style */
        .stButton > button {
            font-size: 1.15rem;
            padding: 0.75rem 1.2rem;
            margin-bottom: 0.5rem;
            width: 100%;
            text-align: left;
            background-color: white;
            color: black;
            border: 1px solid #ccc;
            border-radius: 6px;
            transition: background-color 0.2s ease;
        }

        .stButton > button:hover {
            background-color: #f0f2f6;
        }

        /* Make the label above the input box larger */
        div[data-testid="stTextInput"] label {
            font-size: 5.3rem !important;
            font-weight: 600 !important;
        }

        /* Make body text larger */
        p, ul, ol {
            font-size: 1.2rem;
            line-height: 1.6;
        }

         /* Make the search input box taller */
        input[type="text"] {
            height: 3rem !important;
            font-size: 1.1rem !important;
            padding: 0.5rem 1rem !important;
            border: 1px solid #ccc !important;
            border-radius: 6px !important;
            box-shadow: none !important;
        }

    </style>
    """,
    unsafe_allow_html=True
)



# 🎬 Title of your app
st.title("🎬 Dataflix Movie/Show Information Finder")

# 🧠 Set up default page FIRST
if "page" not in st.session_state:
    st.session_state.page = "home"

# 🌐 Sidebar navigation
st.sidebar.title("Navigation")
if st.sidebar.button("🏠 Home / Introduction"):
    st.session_state.page = "home"
if st.sidebar.button("🔍 Search Page"):
    st.session_state.page = "search"
if st.sidebar.button("📈 Tableau Dashboard"):
    st.session_state.page = "tableau"
if st.sidebar.button("📊 Genre Count by Rating"):
    st.session_state.page = "visual1"
if st.sidebar.button("📊 Most Common Genre"):
    st.session_state.page = "visual2"





# 📂 Load the dataset (only when needed)
@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles1.csv")
    return df
# 🏠 Home page (intro text)
if st.session_state.page == "home":
    st.subheader("Welcome to Netflix Movie/Show Information Finder!")
    st.write("""
    This website helps you search for Netflix titles and explore their genres, descriptions, types, and more.
    
             
    ### Features:
    - 🔍 **Search** for any movie or TV show by title prefix
    - 📊 **Visualize** how genres are distributed across the platform       
    - 📈 **Interact** with our Tableau dashboard to see ratings and trends
             


    ### Story:
    Together, these visualizations guide the user from a vague idea to a confident decision, blending exploration, filtering, and discovery in one seamless flow.

    **Searching:**
    Imagine you're opening up this streaming platform, looking for something new to watch. Maybe you have a specific title in mind. Our first visualization helps you search directly by movie or show title, a quick way to find that one series your friend recommended.

    **Filtering:**
    But let’s say nothing specific comes to mind. You decide to narrow things down by what you’re in the mood for, maybe something age-appropriate or more mature. Our second visualization allows you to filter content by rating, making it easy to find PG movies for a family night or TV-MA shows for a solo binge.

    **Filtering the Popular Countries:**
    Now, you want something a little off the beaten path, not another U.S. or U.K. production. Our third visualization helps you filter out the most popular countries to discover hidden gems from places like South Korea, Spain, or Brazil.

    **Genre Count by Rating:**
    Once you’ve narrowed by rating and region, you might wonder, what kind of content is even available? Our fourth visualization shows the distribution of genres by rating, so you can quickly see if there’s a lot of comedy in PG-13, or whether documentaries and thrillers dominate TV-MA.

    **Most Common Genre:**
    Finally, you’re curious about trends. Has horror become more popular in recent years? What genre defined the early 2010s? Our last chart reveals the most common genre by release year, helping you spot patterns and maybe even pick something nostalgic, or on-trend.
     

    **Use the sidebar on the left to start exploring!**
    """)

# 📈 Visualization Image Page
elif st.session_state.page == "visual1":
    st.markdown("### Genre Count by Rating")
    st.image("Genrerate.png", caption="Genre Count by Rating Visualization", use_container_width=True)

elif st.session_state.page == "visual2":
    st.markdown("### Most Common Genre by Release Year")
    st.image("Most Common.png", caption="Genre Distribution Visualization", use_container_width=True)
    

# 📉 Tableau Dashboard Page
elif st.session_state.page == "tableau":
    st.markdown("### Interactive Tableau Dashboard")
    st.markdown(" ")

    st.markdown("""
        <iframe src="https://public.tableau.com/views/FINALWORKINGDataFlix/RatingDashboard?:embed=y&:display_count=yes&:showVizHome=no"
        width="100%" height="700" frameborder="0" allowfullscreen></iframe>
    """, unsafe_allow_html=True)

# 🔍 Search Page
else:
    df = load_data()

    user_input = st.text_input("", placeholder="Search for a movie or show title")
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
