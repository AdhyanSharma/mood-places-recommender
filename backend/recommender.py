import requests

MOOD_TAGS = {
    "happy": ["cafe", "restaurant", "park"],
    "sad": ["park", "library", "temple"],
    "romantic": ["restaurant", "park", "viewpoint"],
    "adventure": ["park", "trail"],
}


def get_places(mood, lat=None, lon=None, user="default"):

    if not lat or not lon:
        return []

    tags = MOOD_TAGS.get(mood.lower(), ["park"])

    places = []

    for tag in tags:

        query = f"""
        [out:json];
        node(around:2000,{lat},{lon})["amenity"="{tag}"];
        out;
        """

       try:
    response = requests.post(
        "https://overpass-api.de/api/interpreter",
        data=query,
        timeout=20,
        headers={"User-Agent": "MoodPlacesApp/1.0"},
    )

    if response.status_code != 200:
        return []

    if not response.text.strip():
        return []

    data = response.json()

except Exception as e:
    print("Overpass API error:", e)
    return []
        data = response.json()

        for item in data.get("elements", []):
            name = item.get("tags", {}).get("name")

            if name:
                places.append({
                    "name": name,
                    "image": f"https://source.unsplash.com/400x300/?{tag}",
                    "map": f"https://maps.google.com/?q={item['lat']},{item['lon']}",
                })

    return places[:12]