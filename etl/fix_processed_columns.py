import pandas as pd, os

ROOT = r"C:\Users\samba\OneDrive\Desktop\Media_Content_Analytics_Platform"
proc = os.path.join(ROOT, "data", "processed")

news_file = os.path.join(proc, "NEWS_yahoo_11cols.csv")
yt_file = os.path.join(proc, "dim_video.csv")


if os.path.exists(news_file):
    df = pd.read_csv(news_file)
    if 'category' not in df.columns:
        df['category'] = "Unknown"
    else:
        df['category'] = df['category'].fillna("Unknown")

    if 'sentiment_label' not in df.columns:
        df['sentiment_label'] = "Unknown"
    else:
        df['sentiment_label'] = df['sentiment_label'].fillna("Unknown")

    df.to_csv(news_file, index=False)
    print(f"Updated news file: {news_file}")
else:
    print("NEWS_yahoo_11cols.csv not found")

# Fix YouTube file
if os.path.exists(yt_file):
    dfy = pd.read_csv(yt_file)
    if 'region' not in dfy.columns:
        if 'country' in dfy.columns:
            dfy['region'] = dfy['country'].fillna("Global")
        else:
            dfy['region'] = "Global"
    else:
        dfy['region'] = dfy['region'].fillna("Global")

    dfy.to_csv(yt_file, index=False)
    print(f"Updated YouTube file: {yt_file}")
else:
    print("dim_video.csv not found")
