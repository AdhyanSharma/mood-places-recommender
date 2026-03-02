import React, { useState } from "react";
import MapView from "./MapView";
import EmotionDetector from "./EmotionDetector";
import { API } from "./api";
import "./index.css";

export default function App() {
    const [mood, setMood] = useState("happy");
    const [places, setPlaces] = useState([]);
    const [reason, setReason] = useState("");
    const [position, setPosition] = useState([21.1458, 79.0882]);
    const [camera, setCamera] = useState(false);
    const [loading, setLoading] = useState(false);

    const distance = (a, b, c, d) => {
        const R = 6371;
        const dLat = ((c - a) * Math.PI) / 180;
        const dLon = ((d - b) * Math.PI) / 180;
        const x =
            Math.sin(dLat / 2) ** 2 +
            Math.cos((a * Math.PI) / 180) *
            Math.cos((c * Math.PI) / 180) *
            Math.sin(dLon / 2) ** 2;
        return (R * (2 * Math.atan2(Math.sqrt(x), Math.sqrt(1 - x)))).toFixed(2);
    };

    const fetchPlaces = async (selectedMood) => {
        setLoading(true);

        navigator.geolocation.getCurrentPosition(async (pos) => {
            const lat = pos.coords.latitude;
            const lng = pos.coords.longitude;

            setPosition([lat, lng]);

            try {
                const res = await API.post("/recommend", { mood: selectedMood, lat, lng });
                setPlaces(res.data.places);
                setReason(res.data.reason);
            } catch (err) {
                console.error(err);
                setReason("Could not retrieve places at this time.");
            }
            setLoading(false);
        }, (err) => {
            console.error("Location error:", err);
            setLoading(false);
            setReason("Please enable location services to find nearby places.");
        });
    };

    return (
        <div className="app-wrapper">
            <h1 className="hero-title">Mood Places Recommender</h1>
            <p className="hero-subtitle">
                Discover the perfect spots around you that match exactly how you feel.
            </p>

            <div className="controls-panel">
                <select className="mood-select" value={mood} onChange={(e) => setMood(e.target.value)}>
                    <option value="happy">😄 Happy</option>
                    <option value="sad">😢 Sad</option>
                    <option value="relaxed">🧘 Relaxed</option>
                    <option value="excited">🔥 Excited</option>
                </select>

                <button className="primary-btn" onClick={() => fetchPlaces(mood)}>
                    Find Places
                </button>
                <button className="secondary-btn" onClick={() => setCamera(!camera)}>
                    {camera ? "Close Camera" : "🤖 Detect Mood"}
                </button>
            </div>

            {camera && <EmotionDetector onMood={(detected) => { setMood(detected); fetchPlaces(detected); }} />}

            {loading && (
                <div className="loading-indicator">
                    <div className="spinner"></div> Finding places for your vibe...
                </div>
            )}

            {reason && !loading && (
                <div className="reason-box">
                    <span className="reason-icon">💡</span>
                    <div>{reason}</div>
                </div>
            )}

            {!loading && places.length > 0 && (
                <div className="content-grid">
                    <div className="map-wrapper">
                        <MapView places={places} position={position} />
                    </div>

                    <div className="cards-list">
                        {places.map((p, i) => (
                            <div className="place-card" key={i}>
                                <h3 className="place-name">{p.name}</h3>
                                <div className="place-meta">
                                    <div className="place-distance">
                                        <span>📍</span> {distance(position[0], position[1], p.lat, p.lng)} km away
                                    </div>
                                    {p.rating && (
                                        <div className="place-rating">
                                            ★ {p.rating}
                                        </div>
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}