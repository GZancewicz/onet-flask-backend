#!/usr/bin/python3
import requests
import json
import os
from youtube_credentials import get_api_key

# Constants
# YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY"  # Replace with your API key
CHANNEL_ID = "UCb_MxJmD_J4peQtRHj-qBKA"  # Replace with the channel ID of @orthodoxnet
SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
VIDEOS_URL = "https://www.googleapis.com/youtube/v3/videos"
MAX_RESULTS = 100


def fetch_last_videos(api_key, channel_id, max_results):
    # Fetch video IDs first
    params = {
        "key": get_api_key(),
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


if __name__ == "__main__":
    # Fetch new videos
    new_videos = fetch_last_videos(get_api_key(), CHANNEL_ID, MAX_RESULTS)
    print(f"Fetched {len(new_videos)} new videos.")

    # For debugging: print the first new video title
    if new_videos:
        print(f"First new video title: {new_videos[0]['title']}")

    # Check if videos.json exists
    filepath = "./content/videos.json"
    if os.path.exists(filepath):
        # Read existing videos from videos.json
        with open(filepath, "r", encoding="utf-8") as f:
            existing_videos = json.load(f)
        print(f"Found {len(existing_videos)} existing videos.")

        # For debugging: print the first existing video title
        if existing_videos:
            print(f"First existing video title: {existing_videos[0]['title']}")

        # Prepend new videos to existing videos
        new_videos = new_videos + existing_videos  # Prepending new videos
    else:
        print("No existing videos found.")

    # Save the updated videos list back to videos.json
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(new_videos, f, ensure_ascii=False, indent=4)

    print(f"{len(new_videos)} videos saved to {filepath}.")
