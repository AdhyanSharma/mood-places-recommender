from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from textblob import TextBlob
from recommender import get_places
from learning import add_feedback

app = FastAPI()

# Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Mood Places API Running"}


# health check (for warmup + uptime robot)
@app.get("/health")
def health():
    return {"status": "ok"}


# intelligent recommendation
@app.get("/recommend/{mood}")
def recommend(
    mood: str,
    lat: float = None,
    lon: float = None,
    user: str = "default",
):
    results = get_places(mood, lat, lon, user)
    return {"results": results}


# NLP mood detection
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


# learning feedback
@app.post("/feedback")
def feedback(data: dict):

    user = data.get("user", "default")
    category = data.get("category")

    if category:
        add_feedback(user, category)

    return {"message": "Preference learned"}