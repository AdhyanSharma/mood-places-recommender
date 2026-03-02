import React, { useRef } from "react";
import Webcam from "react-webcam";
import { API } from "./api";

export default function EmotionDetector({ onMood }) {
    const webcamRef = useRef(null);

    const capture = async () => {
        const image = webcamRef.current.getScreenshot();
        if (!image) return;
        try {
            const res = await API.post("/detect_mood", { image });
            if (res.data.mood) {
                onMood(res.data.mood);
            }
        } catch (error) {
            console.error("Failed to detect mood:", error);
        }
    };

    return (
        <div className="detector-container">
            <h3>Analyze My Vibe</h3>
            <p style={{ color: "var(--text-muted)", marginBottom: "16px", fontSize: "0.95rem" }}>
                Look at the camera and snap a photo to instantly find places that match your facial expression!
            </p>
            <Webcam
                ref={webcamRef}
                screenshotFormat="image/jpeg"
                className="webcam-view"
                videoConstraints={{ facingMode: "user" }}
            />
            <br />
            <button className="primary-btn" onClick={capture} style={{ width: "100%" }}>
                📸 Snap & Detect
            </button>
        </div>
    );
}