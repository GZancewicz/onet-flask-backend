#!/usr/bin/python3
import json
import requests
from youtube_credentials import get_api_key

# Constants
# YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY"  # Replace with your API key
CHANNEL_ID = "UCb_MxJmD_J4peQtRHj-qBKA"  # Replace with the channel ID of @orthodoxnet
SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
VIDEOS_URL = "https://www.googleapis.com/youtube/v3/videos"
PLAYLIST_URL = "https://www.googleapis.com/youtube/v3/playlistItems"
MAX_RESULTS = 20
HOMILIES_PLAYLIST = "PLEh2brXYUf7kJYXxrBKAxXSKYdl46IHde"
CHILDRENS_PLAYLIST = "PLEh2brXYUf7nIigGqPthPFw4ApKiIu9zW"
CATECHISM_PLAYLIST = "PLEh2brXYUf7k06I4K0dgAJC11A3TlgpFK"


def fetch_homilies_playlist(max_results=MAX_RESULTS):
    return fetch_latest_playlist_videos(HOMILIES_PLAYLIST, max_results)


def fetch_childrens_playlist(max_results=MAX_RESULTS):
    return fetch_latest_playlist_videos(CHILDRENS_PLAYLIST, max_results)


def fetch_catechism_playlist(max_results=MAX_RESULTS):
    return fetch_latest_playlist_videos(CATECHISM_PLAYLIST, max_results)


def fetch_video_data(video_ids):
    params = {
        "key": get_api_key(),
        "id": ",".join(video_ids),
        "part": "snippet,statistics,contentDetails",
    }
    response = requests.get(VIDEOS_URL, params=params)
    response_data = response.json()

    return response_data


def fetch_playlist_video_ids(playlist_id, max_results):
    params = {
        "key": get_api_key(),
        "playlistId": playlist_id,
        "order": "date",
        "part": "snippet",
        "maxResults": max_results,
    }
    response = requests.get(PLAYLIST_URL, params=params)
    response_data = response.json()

    video_ids = [
        item["snippet"]["resourceId"]["videoId"] for item in response_data["items"]
    ]
    return video_ids


def fetch_latest_playlist_videos(playlist_id, max_results=MAX_RESULTS):
    video_ids = fetch_playlist_video_ids(playlist_id, max_results)
    response_data = fetch_video_data(video_ids)

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


def fetch_latest_video_ids(
    api_key=get_api_key(), channel_id=CHANNEL_ID, max_results=MAX_RESULTS
):
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

    return video_ids


def fetch_latest_videos(
    api_key=get_api_key(), channel_id=CHANNEL_ID, max_results=MAX_RESULTS
):
    video_ids = fetch_latest_video_ids(api_key, channel_id, max_results)

    # # Fetch video IDs first
    # params = {
    #     "key": api_key,
    #     "channelId": channel_id,
    #     "order": "date",
    #     "part": "snippet",
    #     "type": "video",
    #     "maxResults": max_results,
    # }
    # response = requests.get(SEARCH_URL, params=params)
    # response_data = response.json()

    # if "items" not in response_data:
    #     print(
    #         "Error fetching videos:",
    #         response_data.get("error", {}).get("message", "Unknown error"),
    #     )
    #     return []

    # video_ids = [item["id"]["videoId"] for item in response_data["items"]]

    # # Fetch video details
    # params = {
    #     "key": api_key,
    #     "id": ",".join(video_ids),
    #     "part": "snippet,statistics,contentDetails",
    # }
    # response = requests.get(VIDEOS_URL, params=params)
    # response_data = response.json()

    response_data = fetch_video_data(video_ids)

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


# if __name__ == "__main__":
#     latest_videos = fetch_catechism_playlist()
#     # latest_videos = fetch_latest_videos()
#     print(json.dumps(latest_videos, indent=2))
