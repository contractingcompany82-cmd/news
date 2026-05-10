import streamlit as st
import feedparser

st.set_page_config(page_title="Auto News RSS", page_icon="📰", layout="wide")

st.title("📰 Auto-Updating RSS News Website")

st.caption("This page auto-refreshes automatically based on the time you set in the sidebar.")

st.sidebar.header("Settings")

rss_url = st.sidebar.text_input(
    "RSS Feed URL",
    value="https://feeds.bbci.co.uk/news/world/rss.xml"
)

refresh_seconds = st.sidebar.slider("Auto refresh (seconds)", 30, 300, 60)

# Simple auto-refresh using HTML meta tag
st.markdown(
    f"""
    <meta http-equiv="refresh" content="{refresh_seconds}">
    """,
    unsafe_allow_html=True,
)

st.sidebar.write(f"⏱️ Page refreshes every **{refresh_seconds}** seconds.")

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
