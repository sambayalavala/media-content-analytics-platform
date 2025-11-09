#  Media Content Analytics Platform (MCAP)

##  Overview

The **Media Content Analytics Platform (MCAP)** is an end-to-end data analytics solution that integrates **YouTube** and **News** datasets to generate actionable insights.  
It helps users understand **media trends**, **audience engagement**, and **sentiment analysis** through an interactive dashboard.  

This project demonstrates how to **extract**, **clean**, **transform**, and **visualize** large-scale data using **Python**, **Streamlit**, **MySQL**, and **Google BigQuery**.

---

##  Tech Stack

| Category | Technologies Used |
|-----------|-------------------|
| **Programming Language** | Python 3.13 |
| **Dashboard Framework** | Streamlit |
| **Visualization Libraries** | Plotly, PyDeck |
| **Data Processing** | Pandas, NumPy |
| **Databases** | MySQL, Google BigQuery |
| **Cloud Platform** | Google Cloud Platform (GCP) |
| **APIs Used** | YouTube Data API |
| **Tools** | PyCharm, Jupyter Notebook |

---

---

##  Features

###  YouTube Analytics
- Fetch and analyze trending videos.  
- Display top 10 videos by view count.  
- Filter by region (Global, India, US, UK, etc.).  
- Visualize views, likes, and comments.

###  News Analytics
- Analyze news sentiment (Positive, Neutral, Negative).  
- Show category-wise article count.  
- Display top trending news articles.  
- Compare YouTube and News data side by side.

###  Dashboard
- Interactive charts and tables.  
- Combined KPIs for YouTube and News datasets.  
- Modern, user-friendly interface with filters.  

---

##  Setup Instructions

###  Step 1: Clone the Repository

git clone https://github.com/sambayalavala/media-content-analytics-platform.git
cd media-content-analytics-platform

###  Step 2: Install Dependencies
pip install -r requirements.txt

###  Step 3: Configure Credentials
1.Create a folder named config/ in the project root.

2.Add your API keys or configuration files securely (DO NOT push to GitHub).

Example:

config/youtube_api_key.json

config/news_api_key.json
3.Ensure .gitignore contains:
config/*.json

###  Step 4: Run the Dashboard
streamlit run streamlit_app/Dashboards/app.py
Then open in your browser:
👉 http://localhost:8501

###   Dashboard Insights
 ##   YouTube Section

Displays top trending videos with region filters.

Bar charts for views, likes, and engagement.

Lists Top 10 videos by performance.

### News Section

Pie chart for sentiment analysis.

Bar chart for category distribution.

Lists Top trending news articles dynamically.

### Combined Metrics

Total number of YouTube videos.

Total view counts and news articles.

Data preview combining both sources.

### Security

Sensitive files are excluded from version control using .gitignore.

# Sensitive data and cache
config/*.json
__pycache__/
.ipynb_checkpoints/
.DS_Store
Thumbs.db

### Future Enhancements

Add automatic scheduling for real-time data updates.

Integrate YouTube Data API v3 for live tracking.

Add Plotly Mapbox for location-based visualization.

Deploy the dashboard on Google Cloud Run or Streamlit Cloud.

### Author

## Sambasivarao Yalavala
 B.Tech – CSE (AI), Dr. MGR Educational and Research Institute
 Data Engineering & Cloud Enthusiast
 GitHub: https://github.com/sambayalavala
