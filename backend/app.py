from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import base64
import numpy as np
import cv2
from deepface import DeepFace

app = Flask(__name__)
CORS(app)

# ---------------- MOOD MAP ----------------
MOOD_MAP = {
    "happy": ["cafe","restaurant","park"],
    "sad": ["park","temple"],
    "relaxed": ["garden","museum"],
    "excited": ["mall","cinema"]
}

MOOD_REASON = {
    "happy": "Social places enhance positive emotions.",
    "sad": "Nature helps improve emotional wellbeing.",
    "relaxed": "Peaceful environments maintain calmness.",
    "excited": "Entertainment places match energetic moods."
}

# ---------------- OVERPASS QUERY ----------------
def get_places(lat, lon, keyword):

    query = f"""
    [out:json][timeout:25];
    (
      node(around:3000,{lat},{lon})["amenity"="{keyword}"];
      node(around:3000,{lat},{lon})["leisure"="{keyword}"];
      node(around:3000,{lat},{lon})["tourism"="{keyword}"];
      node(around:3000,{lat},{lon})["shop"="{keyword}"];
    );
    out;
    """

    servers = [
        "https://overpass-api.de/api/interpreter",
        "https://overpass.kumi.systems/api/interpreter",
        "https://lz4.overpass-api.de/api/interpreter"
    ]

    data=None

    for url in servers:
        try:
            res = requests.post(
                url,
                data=query,
                headers={"User-Agent":"MoodApp"},
                timeout=20
            )
            if res.status_code==200:
                data=res.json()
                break
        except:
            continue

    if not data:
        return []

    places=[]
    for p in data.get("elements",[])[:10]:
        places.append({
            "name":p.get("tags",{}).get("name",keyword.title()),
            "lat":p["lat"],
            "lng":p["lon"],
            "rating":"4."+str(np.random.randint(1,9))
        })

    return places


# ---------------- RECOMMEND ROUTE ----------------
@app.route("/recommend",methods=["POST"])
def recommend():
    try:
        data=request.json
        mood=data["mood"]
        lat=float(data["lat"])
        lon=float(data["lng"])

        types=MOOD_MAP.get(mood,["cafe"])

        results=[]
        for t in types:
            results.extend(get_places(lat,lon,t))

        # fallback demo places
        if len(results)==0:
            results=[
                {"name":"Local Cafe","lat":lat+0.002,"lng":lon+0.002,"rating":"4.2"},
                {"name":"City Park","lat":lat-0.002,"lng":lon-0.002,"rating":"4.5"}
            ]

        return jsonify({
            "places":results,
            "reason":MOOD_REASON.get(mood)
        })

    except Exception as e:
        print("Error:",e)
        return jsonify({"places":[],"reason":"Fallback recommendation"})


# ---------------- AI MOOD DETECTION ----------------
@app.route("/detect_mood",methods=["POST"])
def detect_mood():
    try:
        img_data=request.json["image"].split(",")[1]
        img_bytes=base64.b64decode(img_data)

        arr=np.frombuffer(img_bytes,np.uint8)
        img=cv2.imdecode(arr,cv2.IMREAD_COLOR)

        result=DeepFace.analyze(img,actions=["emotion"],enforce_detection=False)
        emotion=result[0]["dominant_emotion"]

        mapping={
            "happy":"happy",
            "sad":"sad",
            "neutral":"relaxed",
            "surprise":"excited"
        }

        return jsonify({"mood":mapping.get(emotion,"happy")})

    except:
        return jsonify({"mood":"happy"})


@app.route("/")
def home():
    return "Mood Places Backend Running"


if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)