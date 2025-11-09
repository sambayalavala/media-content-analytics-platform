# etl/add_coordinates.py
import pandas as pd, os
from geopy.geocoders import Nominatim
import time

ROOT = r"C:\Users\samba\OneDrive\Desktop\Media_Content_Analytics_Platform"
proc = os.path.join(ROOT, "data", "processed")

news_path = os.path.join(proc, "NEWS_yahoo_11cols.csv")
yt_path = os.path.join(proc, "dim_video.csv")

geolocator = Nominatim(user_agent="mcap_app")

def add_coords(df, location_col):
    lats, lons = [], []
    for loc in df[location_col].fillna("").tolist():
        try:
            geo = geolocator.geocode(loc, timeout=5)
            if geo:
                lats.append(geo.latitude)
                lons.append(geo.longitude)
            else:
                lats.append(None)
                lons.append(None)
        except:
            lats.append(None)
            lons.append(None)
        time.sleep(1)  # avoid API rate limit
    df["latitude"] = lats
    df["longitude"] = lons
    return df

# NEWS dataset
if os.path.exists(news_path):
    df = pd.read_csv(news_path)
    if "latitude" not in df.columns and "location" in df.columns:
        df = add_coords(df, "location")
        df.to_csv(news_path, index=False)
        print("✅ Added coordinates to NEWS file.")

# YouTube dataset
if os.path.exists(yt_path):
    dfy = pd.read_csv(yt_path)
    if "latitude" not in dfy.columns and "region" in dfy.columns:
        dfy = add_coords(dfy, "region")
        dfy.to_csv(yt_path, index=False)
        print("✅ Added coordinates to YouTube file.")
