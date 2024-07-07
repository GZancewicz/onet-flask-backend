from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json

from fetch_youtube import (
    fetch_latest_videos,
    fetch_childrens_playlist,
    fetch_catechism_playlist,
    fetch_homilies_playlist,
)
from fetch_calendar import return_calendar_events
from fetch_ghost import fetch_article, fetch_tagged_posts, fetch_tagged_post_data


app = Flask(__name__)
CORS(app)


@app.route("/heartbeat", methods=["GET"])
def heartbeat():
    return jsonify({"status": "ok"}), 200


@app.route("/test_article", methods=["GET"])
def get_test_article():
    article = fetch_article("652a8f969a71080001718f5b")
    if article:
        return jsonify(article), 200
    else:
        return jsonify({"error": "No article content found"}), 404


@app.route("/onet_articles_to_list", methods=["GET"])
def get_article_list_to_list():
    article_list = fetch_tagged_posts("orthodox_net")

    if not article_list:
        return jsonify({"error": "No articles found"}), 404

    filtered_articles = [
        {
            "id": article["id"],
            "primary_tag_slug": article["primary_tag"]["slug"],
            "title": article["title"],
            "excerpt": article["excerpt"],
        }
        for article in article_list.get("posts", [])
        if article["primary_tag"]["name"].startswith("onet_")
    ]

    return jsonify(filtered_articles), 200


@app.route("/onet_articles", methods=["GET"])
def get_article_list():
    article_list = fetch_tagged_posts("orthodox_net")
    if article_list:
        return jsonify(article_list), 200
    else:
        return jsonify({"error": "No articles found"}), 404


@app.route("/onet_article_data", methods=["GET"])
def get_article_data():
    article_list = fetch_tagged_post_data("orthodox_net")
    if article_list:
        return jsonify(article_list), 200
    else:
        return jsonify({"error": "No articles found"}), 404


@app.route("/onet_article", methods=["GET"])
def get_onet_article():
    article_id = request.args.get("article_id")
    if not article_id:
        return jsonify({"error": "article_id parameter is required"}), 400
    article = fetch_article(article_id)
    if article:
        return jsonify(article), 200
    else:
        return jsonify({"error": "No article content found for the provided ID"}), 404


@app.route("/latest_article", methods=["GET"])
def get_latest_article():
    articles = get_article_list()
    article_id = request.args.get("article_id")
    if not article_id:
        return jsonify({"error": "article_id parameter is required"}), 400
    article = fetch_article(article_id)
    if article:
        return jsonify(article), 200
    else:
        return jsonify({"error": "No article content found for the provided ID"}), 404


@app.route("/schedule", methods=["GET"])
def get_latest_schedule():
    latest_schedule = return_calendar_events()
    if latest_schedule:
        return jsonify(latest_schedule), 200
    else:
        return jsonify({"error": "No schedule found"}), 404


@app.route("/latest_videos", methods=["GET"])
def get_latest_videos():
    latest_videos = fetch_latest_videos()
    if latest_videos:
        return jsonify(latest_videos), 200
    else:
        return jsonify({"error": "No videos found"}), 404


@app.route("/childrens_videos", methods=["GET"])
def get_childrens_videos():
    latest_videos = fetch_childrens_playlist()
    if latest_videos:
        return jsonify(latest_videos), 200
    else:
        return jsonify({"error": "No videos found"}), 404


@app.route("/catechism_videos", methods=["GET"])
def get_catechism_videos():
    latest_videos = fetch_catechism_playlist()
    if latest_videos:
        return jsonify(latest_videos), 200
    else:
        return jsonify({"error": "No videos found"}), 404


@app.route("/homilies_videos", methods=["GET"])
def get_homilies_videos():
    latest_videos = fetch_homilies_playlist()
    if latest_videos:
        return jsonify(latest_videos), 200
    else:
        return jsonify({"error": "No videos found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
