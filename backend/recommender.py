import requests
from sentence_transformers import SentenceTransformer, util
from learning import get_user_bonus

# Load AI model once
model = SentenceTransformer("all-MiniLM-L6-v2")

MOOD_DESCRIPTIONS = {
    "happy": "fun lively energetic social places",
    "sad": "calm peaceful quiet relaxing places",
    "romantic": "beautiful scenic intimate places",
    "adventure": "exciting outdoor exploration activities",
}


# Fetch nearby places from OpenStreetMap
def fetch_nearby(lat, lon):

    query = f"""
    [out:json];
    node(around:2000,{lat},{lon})["amenity"];
    out;
    """

    response = requests.post(
        "https://overpass-api.de/api/interpreter",
        data=query,
    )

    data = response.json()
    places = []

    for item in data.get("elements", []):
        name = item.get("tags", {}).get("name")
        category = item.get("tags", {}).get("amenity")

        if name and category:
            places.append({
                "name": name,
                "category": category,
                "image": f"https://source.unsplash.com/400x300/?{category}",
                "map": f"https://maps.google.com/?q={item['lat']},{item['lon']}",
            })

    return places


# Intelligent + learning recommender
def get_places(mood, lat=None, lon=None, user="default"):

    if not lat or not lon:
        return []

    places = fetch_nearby(lat, lon)

    mood_text = MOOD_DESCRIPTIONS.get(mood, "interesting places")

    mood_embedding = model.encode(
        mood_text, convert_to_tensor=True
    )

    scored_places = []

    for place in places:

        place_embedding = model.encode(
            place["category"], convert_to_tensor=True
        )

        base_score = util.cos_sim(
            mood_embedding, place_embedding
        ).item()

        # learning bonus
        bonus = get_user_bonus(user, place["category"])

        final_score = base_score + (0.05 * bonus)

        place["score"] = final_score
        scored_places.append(place)

    scored_places.sort(key=lambda x: x["score"], reverse=True)

    return scored_places[:12]