from sentence_transformers import SentenceTransformer, util
import requests

# Load AI model once
model = SentenceTransformer("all-MiniLM-L6-v2")

MOOD_DESCRIPTIONS = {
    "happy": "fun lively energetic social places",
    "sad": "calm peaceful quiet relaxing places",
    "romantic": "beautiful scenic intimate places",
    "adventure": "exciting outdoor exploration activities",
}

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


def get_places(mood, lat=None, lon=None):

    if not lat or not lon:
        return []

    places = fetch_nearby(lat, lon)

    mood_text = MOOD_DESCRIPTIONS.get(mood, "interesting places")

    # Embed mood
    mood_embedding = model.encode(mood_text, convert_to_tensor=True)

    scored_places = []

    for place in places:
        place_embedding = model.encode(
            place["category"], convert_to_tensor=True
        )

        score = util.cos_sim(mood_embedding, place_embedding).item()

        place["score"] = score
        scored_places.append(place)

    # Rank intelligently
    scored_places.sort(key=lambda x: x["score"], reverse=True)

    return scored_places[:12]