import requests

# Map mood → place categories
MOOD_TAGS = {
    "happy": ["cafe", "restaurant", "park"],
    "sad": ["garden", "temple", "library"],
    "romantic": ["restaurant", "viewpoint", "park"],
    "adventure": ["trail", "hill", "park"]
}

def get_places(mood, lat=None, lon=None):

    if not lat or not lon:
        return []

    tags = MOOD_TAGS.get(mood.lower(), ["park"])

    places = []

    for tag in tags:
        query = f"""
        [out:json];
        node
          ["amenity"="{tag}"]
          (around:2000,{lat},{lon});
        out;
        """

        response = requests.post(
            "https://overpass-api.de/api/interpreter",
            data=query
        )

        data = response.json()

        for item in data.get("elements", []):

            name = item.get("tags", {}).get("name")

            if name:
                places.append({
                    "name": name,
                    "image": "https://source.unsplash.com/400x300/?place",
                    "map": f"https://maps.google.com/?q={item['lat']},{item['lon']}"
                })

    return places[:12]  # limit results