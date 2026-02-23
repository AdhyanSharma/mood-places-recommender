from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import os

app = Flask(__name__)
CORS(app)

# ===============================
# CONFIG
# ===============================
GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY"   # ← paste your key

DB_FILE = "places_db.json"

# ===============================
# MOOD → PLACE TYPE MAP
# ===============================
MOOD_MAP = {
    "happy": ["cafe", "restaurant", "park"],
    "sad": ["park", "hindu_temple", "lake"],
    "relaxed": ["spa", "museum", "garden"],
    "excited": ["shopping_mall", "movie_theater"]
}

# ===============================
# DATABASE FUNCTIONS
# ===============================
def load_places():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_places(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ===============================
# GOOGLE PLACES API
# ===============================
def get_nearby_places(lat, lng, place_type):

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    params = {
        "location": f"{lat},{lng}",
        "radius": 3000,
        "type": place_type,
        "key": GOOGLE_API_KEY
    }

    response = requests.get(url, params=params).json()

    places = []

    for p in response.get("results", [])[:5]:
        places.append({
            "name": p["name"],
            "lat": p["geometry"]["location"]["lat"],
            "lng": p["geometry"]["location"]["lng"],
            "rating": p.get("rating", 0),
            "source": "google"
        })

    return places

# ===============================
# RECOMMEND ROUTE (FRONTEND MATCH)
# ===============================
@app.route("/recommend/<mood>", methods=["GET"])
def recommend(mood):

    lat = request.args.get("lat")
    lng = request.args.get("lon")

    if not lat or not lng:
        return jsonify({"error": "Location missing"}), 400

    lat = float(lat)
    lng = float(lng)

    print(f"Incoming mood: {mood}")
    print(f"Location: {lat}, {lng}")

    types = MOOD_MAP.get(mood, ["cafe"])

    results = []

    for t in types:
        api_places = get_nearby_places(lat, lng, t)
        print(f"{t} -> {len(api_places)} places")
        results.extend(api_places)

    # add user places
    results.extend(load_places())

    print("Total places:", len(results))

    return jsonify({"results": results})

# ===============================
# ADD NEW PLACE
# ===============================
@app.route("/add_place", methods=["POST"])
def add_place():

    data = request.json

    places = load_places()

    data["rating"] = 0
    data["source"] = "user"

    places.append(data)
    save_places(places)

    return jsonify({"message": "Place added successfully"})

# ===============================
# RATE PLACE
# ===============================
@app.route("/rate", methods=["POST"])
def rate_place():

    data = request.json
    places = load_places()

    for p in places:
        if p["name"] == data["name"]:
            p["rating"] = data["rating"]

    save_places(places)

    return jsonify({"message": "Rating updated"})


# ===============================
# RUN SERVER
# ===============================
if __name__ == "__main__":
    app.run(debug=True)