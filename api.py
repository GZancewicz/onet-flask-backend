from flask import Flask, jsonify
import os
import json


app = Flask(__name__)


@app.route("/heartbeat", methods=["GET"])
def heartbeat():
    return jsonify({"status": "ok"}), 200


def find_latest_schedule(folder_path="./data/bulletin/json"):
    # List all files in the folder
    files = [
        f
        for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
    ]

    # Filter JSON files that start with 'schedule_'
    schedule_files = [
        f for f in files if f.startswith("schedule_") and f.endswith(".json")
    ]

    # Sort the files by date
    sorted_files = sorted(schedule_files, reverse=True)

    # Return the latest file
    if sorted_files:
        return sorted_files[0]
    else:
        return None


@app.route("/schedule", methods=["GET"])
def get_latest_schedule():
    latest_file = find_latest_schedule()

    if latest_file:
        folder_path = "./data/bulletin/json"
        with open(os.path.join(folder_path, latest_file), "r") as f:
            schedule = json.load(f)
        return jsonify(schedule), 200
    else:
        return jsonify({"error": "No schedule files found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
