#!/usr/bin/python3
from flask import Flask, jsonify
from flask_cors import CORS
import json
import requests

# See https://ghost.org/docs/content-api

BASE_URL = "https://orthodox-net.ghost.io/ghost/api/content/"
POSTS_ENDPOINT = "/posts/"
TAGS_ENDPOINT = "/tags/"
GHOST_API_KEY = "fc614c68ef24717d70c30606ba"


def posts_url():
    return BASE_URL + POSTS_ENDPOINT


def tags_url():
    return BASE_URL + TAGS_ENDPOINT


def post_url(post_id):
    return BASE_URL + POSTS_ENDPOINT + post_id + "/"


# https://orthodox-net.ghost.io/ghost/api/content/posts/?key=fc614c68ef24717d70c30606ba
def fetch_posts():
    params = {"key": GHOST_API_KEY, "include": "tags,authors"}
    response = requests.get(posts_url(), params=params)
    response_data = response.json()

    return response_data


def fetch_tags():
    params = {"key": GHOST_API_KEY}
    response = requests.get(tags_url(), params=params)
    response_data = response.json()

    return response_data


def fetch_tagged_posts(slug):
    params = {"key": GHOST_API_KEY, "filter": "tag:" + slug, "include": "tags,authors"}
    response = requests.get(posts_url(), params=params)
    response_data = response.json()

    return response_data


def fetch_post(post_id):
    params = {"key": GHOST_API_KEY, "include": "tags,authors"}
    response = requests.get(post_url(post_id), params=params)
    response_data = response.json()

    return response_data


# Override these to allow frontend to control formatting
def reformat_headings(content):
    return (
        content.replace("<h1", "<strong")
        .replace("</h1>", "</strong>")
        .replace("<h2", "<strong")
        .replace("</h2>", "</strong>")
        .replace("<h3", "<strong")
        .replace("</h3>", "</strong>")
        .replace("<h4", "<strong")
        .replace("</h4>", "</strong>")
        .replace("<h5", "<strong")
        .replace("</h5>", "</strong>")
        .replace("<h6", "<strong")
        .replace("</h6>", "</strong>")
    )


def fetch_article(post_id):
    params = {"key": GHOST_API_KEY, "include": "tags,authors"}
    response = requests.get(post_url(post_id), params=params)
    response_data = response.json()
    title = response_data["posts"][0]["title"]
    content = response_data["posts"][0]["html"]
    content = reformat_headings(content)
    return {
        "title": title,
        "content": content,
    }


# if __name__ == "__main__":
# print(json.dumps(fetch_posts(), indent=2))
# print(json.dumps(fetch_tags(), indent=2))
# print(json.dumps(fetch_tagged_posts("orthodox_net"), indent=2))
# print(json.dumps(fetch_post("652a8f969a71080001718f5b"), indent=2))
# print(json.dumps(fetch_article("652a8f969a71080001718f5b"), indent=2))
