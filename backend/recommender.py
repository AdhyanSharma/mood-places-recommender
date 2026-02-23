import requests

MOOD_QUERIES = {
    "happy": ["cafe", "restaurant"],
    "sad": ["park", "place_of_worship"],
    "romantic": ["restaurant", "viewpoint"],
    "adventure": ["tourism", "attraction", "viewpoint"],
}


def search_places(lat, lon, tags):

    places = []

    for tag in tags:
        query = f"""
        [out:json];
        (
          node(around:3000,{lat},{lon})["amenity"="{tag}"];
          node(around:3000,{lat},{lon})["tourism"="{tag}"];
        );
        out;
        """

        try:
            r = requests.post(
                "https://overpass-api.de/api/interpreter",
                data=query,
                timeout=20,
                headers={"User-Agent": "MoodPlacesApp"},
            )

            if not r.text.strip():
                continue

            data = r.json()

        except:
            continue

        for el in data.get("elements", []):
            name = el.get("tags", {}).get("name")

            if name:
                places.append({
                    "name": name,
                    "lat": el["lat"],
                    "lon": el["lon"],
                    "image": f"https://source.unsplash.com/400x300/?{tag}",
                    "map": f"https://maps.google.com/?q={el['lat']},{el['lon']}",
                })

    return places