from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from textblob import TextBlob
from recommender import get_places

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- STORAGE ----------------
user_places = []
ratings = {}
reviews = {}

# ---------------- BASIC ----------------

@app.get("/")
def home():
    return {"message": "Mood Places API Running"}

@app.get("/health")
def health():
    return {"status": "ok"}

# ---------------- MOOD AI ----------------

@app.get("/detect_mood/{text}")
def detect_mood(text: str):

    polarity = TextBlob(text).sentiment.polarity

    if polarity > 0.3:
        mood = "happy"
    elif polarity < -0.3:
        mood = "sad"
    else:
        mood = "romantic"

    return {"mood": mood}

# ---------------- RECOMMEND ----------------

@app.get("/recommend/{mood}")
def recommend(mood: str, lat: float = None, lon: float = None):

    places = get_places(mood, lat, lon)

    all_places = places + user_places

    # attach rating info
    for p in all_places:
        name = p["name"]
        r = ratings.get(name, [])
        p["rating"] = round(sum(r)/len(r), 1) if r else 0
        p["reviews"] = reviews.get(name, [])

    return {"results": all_places}

# ---------------- ADD PLACE ----------------

@app.post("/add_place")
def add_place(place: dict):
    user_places.append(place)
    return {"message": "Place added"}

# ---------------- ADD RATING ----------------

@app.post("/rate")
def rate_place(data: dict):

    name = data["name"]
    rating = float(data["rating"])

    if name not in ratings:
        ratings[name] = []

    ratings[name].append(rating)

    return {"message": "Rating added"}

# ---------------- ADD REVIEW ----------------

@app.post("/review")
def add_review(data: dict):

    name = data["name"]
    text = data["review"]

    if name not in reviews:
        reviews[name] = []

    reviews[name].append(text)

    return {"message": "Review added"}