#!/usr/bin/python3
import requests
from youtube_credentials import get_api_key

# Constants
# YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY"  # Replace with your API key
CHANNEL_ID = "UCb_MxJmD_J4peQtRHj-qBKA"  # Replace with the channel ID of @orthodoxnet
SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
VIDEOS_URL = "https://www.googleapis.com/youtube/v3/videos"
MAX_RESULTS = 100


def fetch_latest_videos(
    api_key=get_api_key(), channel_id=CHANNEL_ID, max_results=MAX_RESULTS
):
    # Fetch video IDs first
    params = {
        "key": api_key,
        "channelId": channel_id,
        "order": "date",
        "part": "snippet",
        "type": "video",
        "maxResults": max_results,
    }
    response = requests.get(SEARCH_URL, params=params)
    response_data = response.json()

    if "items" not in response_data:
        print(
            "Error fetching videos:",
            response_data.get("error", {}).get("message", "Unknown error"),
        )
        return []

    video_ids = [item["id"]["videoId"] for item in response_data["items"]]

    # Fetch video details
    params = {
        "key": api_key,
        "id": ",".join(video_ids),
        "part": "snippet,statistics,contentDetails",
    }
    response = requests.get(VIDEOS_URL, params=params)
    response_data = response.json()

    videos = []

    for item in response_data["items"]:
        video_data = {
            "title": item["snippet"]["title"],
            "description": item["snippet"]["description"],
            "url": f"https://www.youtube.com/watch?v={item['id']}",
            "thumbnail": item["snippet"]["thumbnails"]["high"]["url"],
            "published_at": item["snippet"]["publishedAt"],
            "channel_title": item["snippet"]["channelTitle"],
            "duration": item["contentDetails"]["duration"],
            "view_count": item["statistics"]["viewCount"],
            "like_count": item["statistics"].get("likeCount", "N/A"),
            "dislike_count": item["statistics"].get("dislikeCount", "N/A"),
        }
        videos.append(video_data)

    return videos
