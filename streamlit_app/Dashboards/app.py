import os
import sys
import pandas as pd
import streamlit as st
import plotly.express as px

# Run check for safety
if __name__ == "__main__" and ("streamlit" not in " ".join(sys.argv).lower()):
    print("⚠ Please run using: streamlit run streamlit_app/Dashboards/app.py")
    sys.exit(0)

# Page setup
st.set_page_config(page_title="Media Content Analytics Platform", page_icon="🌍", layout="wide")

# Custom dark theme
st.markdown("""
    <style>
    .stApp {background-color: #0f1720; color: #e6eef6;}
    h1, h2, h3, h4 {color: #7bdff6;}
    </style>
""", unsafe_allow_html=True)

# Title and intro
st.title("🌍 Media Content Analytics Platform")
st.markdown("Analyze *YouTube* and *Yahoo News* data together — regions, categories, and engagement trends.")

# File paths
ROOT = r"C:\Users\samba\OneDrive\Desktop\Media_Content_Analytics_Platform"
DATA_PATH = os.path.join(ROOT, "data", "processed")
YT_FILE = os.path.join(DATA_PATH, "dim_video.csv")
NEWS_FILE = os.path.join(DATA_PATH, "NEWS_yahoo_11cols.csv")

# Load data safely
@st.cache_data(ttl=300)
def load_data():
    yt_df = pd.read_csv(YT_FILE) if os.path.exists(YT_FILE) else pd.DataFrame()
    news_df = pd.read_csv(NEWS_FILE) if os.path.exists(NEWS_FILE) else pd.DataFrame()
    return yt_df, news_df

yt_df, news_df = load_data()

# Clean column names
yt_df.columns = yt_df.columns.str.lower()
news_df.columns = news_df.columns.str.lower()

# Default region data (if missing)
default_regions = ["Global", "India", "USA", "UK", "Germany", "Japan", "Australia"]
if "region" not in yt_df.columns:
    yt_df["region"] = pd.Series(default_regions * (len(yt_df) // len(default_regions) + 1))[:len(yt_df)]

# Sidebar filters
st.sidebar.header("🔍 Filters")
categories = news_df["category"].dropna().unique().tolist() if "category" in news_df.columns else []
regions = yt_df["region"].dropna().unique().tolist() if "region" in yt_df.columns else []

selected_cat = st.sidebar.multiselect("📰 Choose News Category", categories)
selected_region = st.sidebar.multiselect("🎥 Choose YouTube Region", regions, default=["Global"])

if selected_cat:
    news_df = news_df[news_df["category"].isin(selected_cat)]
if selected_region:
    yt_df = yt_df[yt_df["region"].isin(selected_region)]

if st.sidebar.button("🔄 Refresh"):
    st.cache_data.clear()
    st.rerun()

# KPI Metrics
st.markdown("### 📊 Key Metrics Overview")
k1, k2, k3 = st.columns(3)
k1.metric("Total YouTube Videos", len(yt_df))
k2.metric("Total News Articles", len(news_df))
k3.metric("Total YouTube Views", int(yt_df["views"].sum()) if "views" in yt_df.columns else "N/A")

# YouTube Dashboards
st.subheader("🎥 YouTube Insights")

if not yt_df.empty and "views" in yt_df.columns:
    yt_df["views"] = pd.to_numeric(yt_df["views"], errors="coerce").fillna(0)

    left, right = st.columns(2)

    # ⿡ Top Trending Videos (Bar)
    with left:
        top10 = yt_df.sort_values("views", ascending=False).head(10)
        fig1 = px.bar(top10, x="title", y="views", color="region", title="Top 10 Trending Videos")
        st.plotly_chart(fig1, use_container_width=True)

    # ⿢ View Share by Channel (Pie)
    with right:
        if "channel_title" not in yt_df.columns:
            yt_df["channel_title"] = "Unknown"
        channel_data = (
            yt_df.groupby("channel_title")["views"].sum().reset_index().sort_values("views", ascending=False).head(8)
        )
        fig2 = px.pie(channel_data, names="channel_title", values="views", title="View Share by Channel")
        st.plotly_chart(fig2, use_container_width=True)

    # Daily Views Trend (Line)
    if "publish_date" in yt_df.columns:
        try:
            yt_df["publish_date"] = pd.to_datetime(yt_df["publish_date"], errors="coerce")
            daily = yt_df.groupby("publish_date")["views"].sum().reset_index()
            fig3 = px.line(daily, x="publish_date", y="views", markers=True, title="📅 Daily Views Trend")
            st.plotly_chart(fig3, use_container_width=True)
        except:
            st.warning("⚠ Error parsing publish_date.")
else:
    st.info("No YouTube data available or 'views' missing.")


# Yahoo News Dashboards
st.subheader("📰 Yahoo News Insights")

if not news_df.empty:
    c1, c2 = st.columns(2)

    # Category Distribution
    with c1:
        if "category" in news_df.columns:
            cat_data = news_df["category"].value_counts().reset_index()
            cat_data.columns = ["category", "count"]
            fig4 = px.bar(cat_data, x="category", y="count", color="category", title="Articles per Category")
            st.plotly_chart(fig4, use_container_width=True)

    # ⿢ Sentiment Pie Chart
    with c2:
        if "sentiment_label" in news_df.columns:
            fig5 = px.pie(news_df, names="sentiment_label", title="Sentiment Distribution")
            st.plotly_chart(fig5, use_container_width=True)

    #  Top News Articles
    st.markdown("### 🔥 Top Trending News Articles")
    display_col = "headline" if "headline" in news_df.columns else "title"
    if display_col in news_df.columns:
        for i, headline in enumerate(news_df[display_col].dropna().head(10), 1):
            st.markdown(f"{i}. {headline}")
else:
    st.info("No News data available.")

# Footer
st.markdown("---")
st.caption("📘 Media Content Analytics Platform | Built by Sambasivarao Yalavala")
