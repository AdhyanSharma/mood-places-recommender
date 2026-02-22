import math

def distance(lat1, lon1, lat2, lon2):
    return math.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)


places_data = {
    "happy": [
        {
            "name": "Futala Lake",
            "lat": 21.141,
            "lon": 79.047,
            "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e",
            "map": "https://maps.google.com/?q=Futala+Lake+Nagpur",
        },
        {
            "name": "Ambazari Garden",
            "lat": 21.129,
            "lon": 79.043,
            "image": "https://images.unsplash.com/photo-1506744038136-46273834b3fb",
            "map": "https://maps.google.com/?q=Ambazari+Garden+Nagpur",
        },
    ],

    "sad": [
        {
            "name": "Japanese Garden",
            "lat": 21.145,
            "lon": 79.088,
            "image": "https://images.unsplash.com/photo-1491553895911-0055eca6402d",
            "map": "https://maps.google.com/?q=Japanese+Garden+Nagpur",
        }
    ],

    "romantic": [
        {
            "name": "Seminary Hills",
            "lat": 21.165,
            "lon": 79.055,
            "image": "https://images.unsplash.com/photo-1501785888041-af3ef285b470",
            "map": "https://maps.google.com/?q=Seminary+Hills+Nagpur",
        }
    ],

    "adventure": [
        {
            "name": "Gorewada Nature Trail",
            "lat": 21.207,
            "lon": 79.037,
            "image": "https://images.unsplash.com/photo-1469474968028-56623f02e42e",
            "map": "https://maps.google.com/?q=Gorewada+Nagpur",
        }
    ],
}


def get_places(mood, user_lat=None, user_lon=None):

    places = places_data.get(mood.lower(), [])

    # Sort by nearest location
    if user_lat and user_lon:
        places = sorted(
            places,
            key=lambda p: distance(user_lat, user_lon, p["lat"], p["lon"])
        )

    return places