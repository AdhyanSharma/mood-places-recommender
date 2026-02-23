from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from textblob import TextBlob
from recommender import search_places, MOOD_QUERIES
import math

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

user_places = []
ratings = {}
reviews = {}

# ---------------- DISTANCE ----------------
def distance(lat1, lon1, lat2, lon2):
    return math.sqrt((lat1-lat2)**2 + (lon1-lon2)**2)

# ---------------- MOOD DETECTION ----------------
@app.get("/detect_mood/{text}")
def detect_mood(text: str):

    p = TextBlob(text).sentiment.polarity

    if p > 0.3:
        return {"mood": "happy"}
    elif p < -0.3:
        return {"mood": "sad"}
    return {"mood": "romantic"}

# ---------------- RECOMMEND ----------------
@app.get("/recommend/{mood}")
def recommend(mood: str, lat: float, lon: float):

    tags = MOOD_QUERIES.get(mood, ["park"])

    places = search_places(lat, lon, tags)

    # add user places nearby only
    for p in user_places:
        if distance(lat, lon, p["lat"], p["lon"]) < 0.05:
            places.append(p)

    # attach rating
    for p in places:
        r = ratings.get(p["name"], [])
        p["rating"] = round(sum(r)/len(r), 1) if r else 0
        p["reviews"] = reviews.get(p["name"], [])

    return {"results": places[:15]}

# ---------------- ADD REAL PLACE ----------------
@app.post("/add_place")
def add_place(place: dict):

    # require coordinates
    if "lat" not in place or "lon" not in place:
        return {"error": "Location required"}

    user_places.append(place)
    return {"message": "Real place added"}

# ---------------- RATE ----------------
@app.post("/rate")
def rate(data: dict):
    ratings.setdefault(data["name"], []).append(data["rating"])
    return {"ok": True}

# ---------------- REVIEW ----------------
@app.post("/review")
def review(data: dict):
    reviews.setdefault(data["name"], []).append(data["review"])
    return {"ok": True}