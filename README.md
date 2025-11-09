Media Content Analytics Platform

Overview

The Media Content Analytics Platform (MCAP) is a complete end-to-end data analytics solution that integrates YouTube and News data for generating insights.
It helps in understanding media trends, audience engagement, and sentiment analysis through an interactive dashboard.
This project demonstrates how to extract, clean, transform, and visualise data using Python, Streamlit, MySQL, and Google BigQuery.

Tech Stack

Programming Language: Python 3.13

Dashboard Framework: Streamlit

Visualization Libraries: Plotly, PyDeck

Data Processing: Pandas, NumPy

Databases: MySQL, Google BigQuery

Cloud Platform: Google Cloud Platform (GCP)

APIs Used: YouTube Data API, Kaggle API

Tools: PyCharm, Jupyter Notebook

Project Structure

Media_Content_Analytics_Platform/
│
├── config/
│   ├── kaggle.json
│   ├── mcap-project-477416-81b2xxxx.json
│
├── data/
│   ├── raw/
│   └── processed/
│       ├── NEWS_yahoo_11cols.csv
│       └── dim_video.csv
│
├── etl/
│   ├── fetch_youtube_data.py
│   ├── transform_clean_data.py
│   ├── load_to_mysql.py
│   └── upload_to_bigquery.py
│
├── streamlit_app/
│   └── Dashboards/
│       └── app.py
│
├── notebooks/
│   └── data_analysis.ipynb
│
├── .gitignore
├── requirements.txt
└── README.md


Features
YouTube Analytics

Fetch and analyze trending videos.

Display top 10 videos by view count.

Filter by region (Global, India, US, UK, etc.).

Visualize views, likes, and comments.

News Analytics

Analyze news sentiment (positive, neutral, negative).

Show category-wise article count.

Display trending news articles.

Compare YouTube and News data together.

Dashboard

Interactive charts and tables.

Combined metrics of YouTube and News data.

Easy-to-use interface with filters.

Setup Instructions
Step 1: Clone the Repository
git clone https://github.com/sambayalavala/media-content-analytics-platform.git
cd media-content-analytics-platform

Step 2: Install Dependencies
pip install -r requirements.txt

Step 3: Configure Credentials

Create a folder named config/ and place your credentials inside:

kaggle.json → Kaggle API key

mcap-project-477416-81b2xxxx.json → Google BigQuery credentials

Ensure .gitignore contains:

config/*.json

Step 4: Run the Dashboard
streamlit run streamlit_app/Dashboards/app.py


Open the browser at:
http://localhost:8501

Dashboard Insights
YouTube Section

Displays top trending videos with region filters.

Shows bar charts for views and engagement.

Lists top 10 videos by performance.

News Section

Displays sentiment pie chart.

Shows category-wise distribution.

Lists top trending news articles.

Combined Metrics

Total number of YouTube videos.

Total views and total news articles.

Data preview combining both datasets.

Security

Sensitive configuration files are excluded from version control using .gitignore:

config/*.json
__pycache__/
.ipynb_checkpoints/
.DS_Store
Thumbs.db

Future Improvements

Add automatic scheduling for data updates.

Integrate YouTube API v3 for real-time tracking.

Add Plotly Mapbox for location-based visualization.

Deploy dashboard on Google Cloud Run.

Author

Sambasivarao Yalavala
B.Tech – CSE (AI), Dr. MGR Educational and Research Institute
Data Engineering & Cloud Enthusiast
GitHub: https://github.com/sambayalavala
