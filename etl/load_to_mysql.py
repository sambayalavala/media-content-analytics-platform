# etl/load_to_mysql.py
import mysql.connector
import pandas as pd
import os
import sys

# ✅ MySQL connection details
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "Samba@1925"   # <-- your MySQL password here
MYSQL_DB = "MEDIA_CONTENT_ANALYTICS"

# ✅ Folder paths (processed data)
base_path = r"C:\Users\samba\OneDrive\Desktop\Media_Content_Analytics_Platform\data\processed"
news_file = os.path.join(base_path, "NEWS_yahoo_11cols.csv")
youtube_file = os.path.join(base_path, "dim_video.csv")

# ✅ Connect to MySQL
try:
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )
    cursor = conn.cursor()
    print("✅ Connected to MySQL database:", MYSQL_DB)
except Exception as e:
    print("❌ Error connecting to MySQL:", e)
    sys.exit(1)

# ✅ 1. Create Yahoo News table
cursor.execute("""
CREATE TABLE IF NOT EXISTS yahoo_news_data (
    id INT PRIMARY KEY,
    headline TEXT,
    news_text LONGTEXT,      -- fixed to handle long text
    sentiment INT,
    source VARCHAR(255),
    category VARCHAR(255),
    publish_date DATE,
    word_count INT,
    char_count INT,
    sentiment_label VARCHAR(50),
    text_length_category VARCHAR(50)
)
""")
print("✅ Table yahoo_news_data ready (LONGTEXT used for news_text).")

# ✅ 2. Create YouTube Data table
cursor.execute("""
CREATE TABLE IF NOT EXISTS youtube_data (
    video_id VARCHAR(100) PRIMARY KEY,
    title TEXT,
    channel_title VARCHAR(255),
    category_id VARCHAR(50),
    publish_time DATETIME,
    views INT,
    likes INT,
    dislikes INT,
    comment_count INT,
    description TEXT,
    region VARCHAR(50)
)
""")
print("✅ Table youtube_data ready.")

# ✅ 3. Load data from CSV files
try:
    print("📥 Loading Yahoo news CSV...")
    news_df = pd.read_csv(news_file)
    print("📥 Loading YouTube CSV...")
    youtube_df = pd.read_csv(youtube_file)
except Exception as e:
    print("❌ Error reading CSV files:", e)
    sys.exit(1)

# ✅ 4. Insert Yahoo news data
print("📤 Inserting Yahoo News records...")
for _, row in news_df.iterrows():
    sql = """
    INSERT INTO yahoo_news_data (
        id, headline, news_text, sentiment, source, category,
        publish_date, word_count, char_count, sentiment_label, text_length_category
    ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    data = tuple(row)
    try:
        cursor.execute(sql, data)
    except mysql.connector.errors.IntegrityError:
        pass  # skip duplicates
    except Exception as e:
        print("⚠️ Error inserting news row:", e)

# ✅ 5. Insert YouTube data (auto-adjust to available columns)
print("📤 Inserting YouTube records...")
youtube_df.columns = [c.lower() for c in youtube_df.columns]  # normalize column names
yt_cols = list(youtube_df.columns)
insert_cols = ",".join(yt_cols)
placeholders = ",".join(["%s"] * len(yt_cols))
sql = f"INSERT INTO youtube_data ({insert_cols}) VALUES ({placeholders})"

for _, row in youtube_df.iterrows():
    data = tuple(row)
    try:
        cursor.execute(sql, data)
    except mysql.connector.errors.IntegrityError:
        pass  # skip duplicates
    except Exception as e:
        print("⚠️ Error inserting YouTube row:", e)

# ✅ 6. Commit and close connection
conn.commit()
cursor.close()
conn.close()

print("\n✅ All records inserted successfully into MEDIA_CONTENT_ANALYTICS!")
sys.stdout.flush()
