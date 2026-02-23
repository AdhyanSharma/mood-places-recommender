from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from deepface import DeepFace
import base64
import numpy as np
import cv2

# CREATE APP FIRST
app = Flask(__name__)

# THEN ENABLE CORS
CORS(app)

# ---------------- MOOD → PLACE TYPES ----------------
MOOD_MAP = {
    "happy": ["cafe", "restaurant", "park"],
    "sad": ["park", "temple"],
    "relaxed": ["garden", "museum"],
    "excited": ["mall", "cinema"]
}

# ---------------- OSM SEARCH ----------------
def get_places(lat, lon, keyword):

    query = f"""
    [out:json][timeout:25];
    (
      node(around:3000,{lat},{lon})["amenity"="{keyword}"];
      node(around:3000,{lat},{lon})["leisure"="{keyword}"];
      node(around:3000,{lat},{lon})["tourism"="{keyword}"];
    );
    out;
    """

    # MULTIPLE SERVERS (fallback system)
    servers = [
        "https://overpass-api.de/api/interpreter",
        "https://overpass.kumi.systems/api/interpreter",
        "https://lz4.overpass-api.de/api/interpreter"
    ]

    data = None

    for url in servers:
        try:
            print("Trying Overpass:", url)

            response = requests.post(
                url,
                data=query,
                headers={"User-Agent": "MoodPlacesApp"},
                timeout=20
            )

            if response.status_code == 200:
                data = response.json()
                break

        except Exception as e:
            print("Server failed:", url)

    if not data:
        return []

    places = []

    for p in data.get("elements", [])[:10]:
        places.append({
            "name": p.get("tags", {}).get("name", keyword.title()),
            "lat": p["lat"],
            "lng": p["lon"],
            "rating": "N/A",
            "photo": None
        })

    return places

# ---------------- RECOMMEND ----------------
@app.route("/recommend", methods=["POST"])
def recommend():

    data = request.json

    mood = data["mood"]
    lat = float(data["lat"])
    lon = float(data["lng"])

    types = MOOD_MAP.get(mood, ["cafe"])

    results = []

    for t in types:
        results.extend(get_places(lat, lon, t))

    return jsonify(results)

# ---------------- AI MOOD ----------------
@app.route("/detect_mood", methods=["POST"])
def detect_mood():

    image = request.json["image"].split(",")[1]

    img_bytes = base64.b64decode(image)
    arr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)

    result = DeepFace.analyze(
        img,
        actions=["emotion"],
        enforce_detection=False
    )

    emotion = result[0]["dominant_emotion"]

    mapping = {
        "happy": "happy",
        "sad": "sad",
        "neutral": "relaxed",
        "surprise": "excited"
    }

    mood = mapping.get(emotion, "happy")

    return jsonify({"mood": mood})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)