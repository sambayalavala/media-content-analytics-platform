import os
from pathlib import Path
import pandas as pd

# CONFIGURE PATHS
ROOT = Path(r"C:\Users\samba\OneDrive\Desktop\Media_Content_Analytics_Platform")
RAW_DIR = ROOT / "data" / "data-raw"
PROC_DIR = ROOT / "data" / "processed"

# ensure processed folder exists
os.makedirs(PROC_DIR, exist_ok=True)

# PROCESS NEWS (Kaggle Yahoo dataset)
news_raw_path = RAW_DIR / "NEWS_YAHOO_stock_prediction_Dataset.csv"
news_out_path = PROC_DIR / "NEWS_yahoo_11cols.csv"

print("Reading news raw:", news_raw_path)
news = pd.read_csv(news_raw_path, dtype=str, encoding='utf-8', low_memory=False)

news.columns = [c.strip() for c in news.columns]

news = news.loc[:, ~news.columns.str.contains("^Unnamed", case=False)]

news_cols = {c:c.lower() for c in news.columns}
news = news.rename(columns=news_cols)

if 'title' in news.columns and 'headline' not in news.columns:
    news = news.rename(columns={'title':'headline'})
if 'content' in news.columns and 'news_text' not in news.columns:
    news = news.rename(columns={'content':'news_text'})
if 'label' in news.columns and 'sentiment' not in news.columns:
    news = news.rename(columns={'label':'sentiment'})

# Add id if missing
if 'id' not in news.columns:
    news.insert(0, 'id', range(1, len(news)+1))

for col in ['headline','news_text','sentiment','source','category','publish_date']:
    if col not in news.columns:
        news[col] = pd.NA

def parse_sentiment(x):
    try:
        return int(float(x))
    except:
        if isinstance(x, str):
            x0 = x.strip().lower()
            if x0 in ('positive','pos','1','+1'): return 1
            if x0 in ('negative','neg','0','-1'): return 0
        return pd.NA

news['sentiment'] = news['sentiment'].apply(parse_sentiment)

news['publish_date'] = pd.to_datetime(news['publish_date'], errors='coerce').dt.date
news['news_text'] = news['news_text'].fillna('')
news['word_count'] = news['news_text'].astype(str).apply(lambda s: len(s.split()))
news['char_count'] = news['news_text'].astype(str).apply(len)
news['sentiment_label'] = news['sentiment'].apply(lambda x: 'Positive' if x==1 else ('Negative' if x==0 else 'Unknown'))
news['text_length_category'] = news['word_count'].apply(lambda w: 'Short' if w<100 else ('Medium' if w<300 else 'Long'))

# Keep the 11 columns in the order requested
news_final_cols = ['id','headline','news_text','sentiment','source','category','publish_date',
                   'word_count','char_count','sentiment_label','text_length_category']
news_out = news[news_final_cols]
news_out.to_csv(news_out_path, index=False, encoding='utf-8')
print("Saved processed news to:", news_out_path)

# 2. PROCESS YOUTUBE (youtube_data.csv)
yt_raw_path = RAW_DIR / "youtube_data.csv"
yt_out_path = PROC_DIR / "dim_video.csv"

print("Reading youtube raw:", yt_raw_path)
yt = pd.read_csv(yt_raw_path, dtype=str, encoding='utf-8', low_memory=False)

yt = yt.loc[:, ~yt.columns.str.contains("^Unnamed", case=False)]
yt.columns = [c.strip().lower() for c in yt.columns]

if 'video_id' not in yt.columns and 'id' in yt.columns:
    yt = yt.rename(columns={'id':'video_id'})

for col in ['views','likes','comment_count','comments','dislikes']:
    if col in yt.columns:
        yt[col] = pd.to_numeric(yt[col], errors='coerce').fillna(0).astype(int)

if 'comment_count' not in yt.columns and 'comments' in yt.columns:
    yt['comment_count'] = yt['comments']
if 'likes' not in yt.columns:
    yt['likes'] = 0
if 'dislikes' not in yt.columns:
    yt['dislikes'] = pd.NA

if 'publish_time' in yt.columns:
    yt['publish_time'] = pd.to_datetime(yt['publish_time'], errors='coerce')
elif 'publish_date' in yt.columns:
    yt['publish_time'] = pd.to_datetime(yt['publish_date'], errors='coerce')
else:
    yt['publish_time'] = pd.NaT

final_cols = ['video_id','title','channel_title','category_id','publish_time','views','likes','dislikes','comment_count','description','region']
final_present = [c for c in final_cols if c in yt.columns]
yt_out = yt[final_present].copy()

yt_out.to_csv(yt_out_path, index=False, encoding='utf-8')
print("Saved processed youtube to:", yt_out_path)

print("\nProcessing complete.")
print("News rows:", len(news_out))
print("YouTube rows:", len(yt_out))
