from googleapiclient.discovery import build
import pandas as pd
import os

#  YouTube API Key
api_key = "AIzaSyCulNEAg4WvgvwG6jJ_AiqNuHKK7DKv320"


youtube = build("youtube", "v3", developerKey=api_key)


search_query = "Technology News"  # You can change topic if you want

# Step 1: Search for videos
search_response = youtube.search().list(
    q=search_query,
    part="id,snippet",
    maxResults=20,
    type="video"
).execute()

video_data = []

# Extract details for each video
for item in search_response["items"]:
    video_id = item["id"]["videoId"]
    title = item["snippet"]["title"]
    published_at = item["snippet"]["publishedAt"]
    channel_title = item["snippet"]["channelTitle"]

    # Get video statistics
    video_response = youtube.videos().list(
        part="statistics,snippet",
        id=video_id
    ).execute()

    stats = video_response["items"][0]["statistics"]

    views = stats.get("viewCount", 0)
    likes = stats.get("likeCount", 0)
    comments = stats.get("commentCount", 0)
    category = item["snippet"].get("categoryId", "Unknown")

    video_data.append({
        "video_id": video_id,
        "title": title,
        "channel_title": channel_title,
        "views": views,
        "likes": likes,
        "comments": comments,
        "category": category,
        "publish_date": published_at
    })

# Save to CSV
df = pd.DataFrame(video_data)

# Use your actual project path
output_path = r"C:\Users\samba\OneDrive\Desktop\Media_Content_Analytics_Platform\data\data-raw\youtube_data.csv"


os.makedirs(os.path.dirname(output_path), exist_ok=True)

df.to_csv(output_path, index=False)
print("youtube_data.csv saved successfully at:", output_path)
