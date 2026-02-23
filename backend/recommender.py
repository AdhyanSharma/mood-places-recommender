import requests

MOOD_TAGS = {
    "happy": ["cafe", "restaurant", "park"],
    "sad": ["park", "library", "place_of_worship"],
    "romantic": ["restaurant", "park", "viewpoint"],
    "adventure": ["park", "viewpoint", "museum", "attraction"],
}


def fetch_places(tag, lat, lon):

    query = f"""
    [out:json];
    (
      node(around:4000,{lat},{lon})["amenity"="{tag}"];
      node(around:4000,{lat},{lon})["tourism"="{tag}"];
      node(around:4000,{lat},{lon})["leisure"="{tag}"];
    );
    out;
    """

    try:
        response = requests.post(
            "https://overpass-api.de/api/interpreter",
            data=query,
            timeout=20,
            headers={"User-Agent": "MoodPlacesApp/1.0"},
        )

        if response.status_code != 200 or not response.text.strip():
            return []

        data = response.json()

    except Exception:
        return []

    results = []

    for item in data.get("elements", []):
        name = item.get("tags", {}).get("name")

        if name:
            results.append({
                "name": name,
                "category": tag,
                "image": f"https://source.unsplash.com/400x300/?{tag}",
                "map": f"https://maps.google.com/?q={item['lat']},{item['lon']}",
            })

    return results


def get_places(mood, lat=None, lon=None):

    if lat is None or lon is None:
        return []

    tags = MOOD_TAGS.get(mood.lower(), ["park"])

    places = []

    for tag in tags:
        places.extend(fetch_places(tag, lat, lon))

    return places[:15]