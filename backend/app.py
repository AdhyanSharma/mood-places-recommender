from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from recommender import get_places
from textblob import TextBlob

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root
@app.get("/")
def home():
    return {"message": "Mood Places API Running"}

# Health endpoint (for warmup + uptime robot)
@app.get("/health")
def health():
    return {"status": "ok"}

# Recommend places
@app.get("/recommend/{mood}")
def recommend(mood: str, lat: float = None, lon: float = None):
    results = get_places(mood, lat, lon)
    return {"results": results}

# AI Mood Detection
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