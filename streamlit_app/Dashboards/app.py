import os
import sys
import streamlit as st
import pandas as pd
import plotly.express as px

# SAFETY CHECK
if __name__ == "__main__" and ("streamlit" not in " ".join(sys.argv).lower()):
    print("\n⚠️  Run this file using:\n")
    print("   streamlit run streamlit_app/Dashboards/app.py\n")
    sys.exit(0)

# PAGE CONFIG
st.set_page_config(
    page_title="Media Content Analytics Platform",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Media Content Analytics Platform")
st.markdown("Real-time analysis of **YouTube** and **News** data — compare regions, categories, and trends interactively.")

# PATHS
ROOT = r"C:\Users\samba\OneDrive\Desktop\Media_Content_Analytics_Platform"
PROC_DIR = os.path.join(ROOT, "data", "processed")
NEWS_CSV = os.path.join(PROC_DIR, "NEWS_yahoo_11cols.csv")
YT_CSV = os.path.join(PROC_DIR, "dim_video.csv")

# LOAD DATA
@st.cache_data(ttl=300)
def load_data(news_path, yt_path):
    news_df = pd.read_csv(news_path) if os.path.exists(news_path) else pd.DataFrame()
    yt_df = pd.read_csv(yt_path) if os.path.exists(yt_path) else pd.DataFrame()
    return news_df, yt_df

news_df, yt_df = load_data(NEWS_CSV, YT_CSV)

# Normalize column names
news_df.columns = [c.lower() for c in news_df.columns]
yt_df.columns = [c.lower() for c in yt_df.columns]

# DEFAULT REGIONS
default_regions = ["Global", "India", "USA", "UK", "Germany", "Japan", "Australia"]
if "region" not in yt_df.columns or yt_df["region"].isna().all():
    yt_df["region"] = pd.Series(default_regions * (len(yt_df) // len(default_regions) + 1))[:len(yt_df)]

# SIDEBAR FILTERS
st.sidebar.header("🔍 Filters")
category_list = sorted(news_df["category"].dropna().unique()) if "category" in news_df.columns else []
region_list = sorted(yt_df["region"].dropna().unique())

selected_category = st.sidebar.multiselect("📰 Select News Category", category_list)
selected_region = st.sidebar.multiselect("🎥 Select YouTube Region", region_list, default=["Global"])

# Apply filters
if selected_category:
    news_df = news_df[news_df["category"].isin(selected_category)]
if selected_region:
    yt_df = yt_df[yt_df["region"].isin(selected_region)]

# REFRESH BUTTON
st.sidebar.markdown("---")
if st.sidebar.button("🔄 Refresh Dashboard"):
    st.cache_data.clear()
    st.rerun()

# KPI SECTION
st.markdown("### 📊 Key Metrics Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Total YouTube Videos", f"{len(yt_df):,}")
col2.metric("Total News Articles", f"{len(news_df):,}")
if "views" in yt_df.columns:
    col3.metric("Total YouTube Views", f"{yt_df['views'].sum():,}")
else:
    col3.metric("Total YouTube Views", "N/A")

# YOUTUBE ANALYTICS
st.markdown("### 🎬 YouTube — Top Trending Videos")
if not yt_df.empty and "views" in yt_df.columns:
    yt_df["views"] = pd.to_numeric(yt_df["views"], errors="coerce").fillna(0)
    top_videos = yt_df.sort_values("views", ascending=False).head(10)
    fig1 = px.bar(
        top_videos,
        x="title" if "title" in yt_df.columns else top_videos.index,
        y="views",
        color="region",
        hover_data=["channel_title"] if "channel_title" in yt_df.columns else None,
        title=f"Top 10 YouTube Videos ({', '.join(selected_region)})"
    )
    st.plotly_chart(fig1, width="stretch")

    if "publish_date" in yt_df.columns:
        try:
            yt_df["publish_date"] = pd.to_datetime(yt_df["publish_date"], errors="coerce")
            daily_views = yt_df.groupby("publish_date")["views"].sum().reset_index()
            fig2 = px.line(
                daily_views,
                x="publish_date",
                y="views",
                title="📅 Daily Views Trend",
                markers=True
            )
            st.plotly_chart(fig2, width="stretch")
        except Exception:
            pass
else:
    st.info("No YouTube data available or missing 'views' column.")

# NEWS INSIGHTS
st.markdown("### 📰 News — Category & Sentiment Insights")
if not news_df.empty:
    col_a, col_b = st.columns(2)

    with col_a:
        if "category" in news_df.columns:
            cat_count = news_df["category"].value_counts().reset_index()
            cat_count.columns = ["category", "count"]
            fig3 = px.bar(
                cat_count,
                x="category",
                y="count",
                color="category",
                title="Articles per News Category",
                labels={"category": "Category", "count": "Article Count"}
            )
            st.plotly_chart(fig3, width="stretch")

    with col_b:
        if "sentiment_label" in news_df.columns:
            fig4 = px.pie(
                news_df,
                names="sentiment_label",
                title="News Sentiment Distribution",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig4, width="stretch")

    # TRENDING NEWS ARTICLES
    st.markdown("### 🔥 Top Trending News Articles")
    if not news_df.empty:
        # Pick a text column (title, headline, or first available string column)
        possible_text_cols = [c for c in news_df.columns if news_df[c].dtype == "object"]
        display_col = "title" if "title" in news_df.columns else (
            "headline" if "headline" in news_df.columns else (
                possible_text_cols[0] if possible_text_cols else None
            )
        )

        if display_col:
            top_articles = news_df[display_col].dropna().head(10).tolist()
            for i, article in enumerate(top_articles, start=1):
                st.markdown(f"**{i}. {article}**")
        else:
            st.info("No text column (title/headline) available to display news articles.")
else:
    st.info("No News data found or not yet processed.")

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("📘 Project: Media Content Analytics Platform — Dashboard by Sambasivarao Yalavala")
