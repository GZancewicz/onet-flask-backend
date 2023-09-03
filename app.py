from flask import Flask, jsonify
from flask_cors import CORS
import os
import json
from fetch_youtube import fetch_latest_videos
from fetch_calendar import return_calendar_events


app = Flask(__name__)
CORS(app)


@app.route("/heartbeat", methods=["GET"])
def heartbeat():
    return jsonify({"status": "ok"}), 200


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
