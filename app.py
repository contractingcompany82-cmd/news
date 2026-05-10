import streamlit as st
import feedparser
from datetime import datetime

st.set_page_config(page_title="Auto News RSS", page_icon="📰", layout="wide")

st.title("📰 Auto-Updating RSS News Website")

# Auto refresh every 60 seconds
st.caption("This page auto-refreshes every 60 seconds.")
st_autorefresh = st.experimental_rerun if False else None  # placeholder to avoid linting

count = st.experimental_get_query_params().get("refresh", [0])[0]
count = int(count) if str(count).isdigit() else 0

# Auto-refresh using st_autorefresh
st_autorefresh = st.experimental_rerun
st.experimental_set_query_params(refresh=count + 1)

st.sidebar.header("Settings")

rss_url = st.sidebar.text_input(
    "RSS Feed URL",
    value="https://feeds.bbci.co.uk/news/world/rss.xml"
)

refresh_seconds = st.sidebar.slider("Auto refresh (seconds)", 30, 300, 60)

st.sidebar.write(f"⏱️ Page refreshes every **{refresh_seconds}** seconds.")
st.sidebar.caption("Change value and rerun to adjust refresh rate.")

# Simple auto-refresh using meta refresh
st.markdown(
    f"""
    <meta http-equiv="refresh" content="{refresh_seconds}">
    """,
    unsafe_allow_html=True,
)

if not rss_url:
    st.warning("Please enter a valid RSS feed URL in the sidebar.")
else:
    try:
        feed = feedparser.parse(rss_url)

        if feed.bozo:
            st.error("Failed to parse RSS feed. Please check the URL.")
        else:
            st.write(f"**Source:** {feed.feed.get('title', 'Unknown')}")

            for entry in feed.entries[:20]:
                with st.container():
                    st.markdown(f"### 🔹 {entry.get('title', 'No title')}")
                    if "published" in entry:
                        st.caption(f"🕒 {entry.published}")
                    if "summary" in entry:
                        st.write(entry.summary)
                    if "link" in entry:
                        st.markdown(f"[Read more]({entry.link})")
                    st.markdown("---")
    except Exception as e:
        st.error(f"Error reading RSS feed: {e}")
