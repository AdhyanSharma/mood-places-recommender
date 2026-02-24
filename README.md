# 🌍 Mood Places Recommender (AI Powered)

An AI-powered web application that recommends **nearby places based on the user's mood** using facial emotion recognition and location-aware recommendations.

This project combines **Computer Vision, AI, Full-Stack Development, and Geolocation Services** to create an intelligent real-world recommendation system.

---

## 🚀 Project Overview

People often struggle to decide where to go when they feel stressed, bored, happy, or excited.

This application solves that problem by:

✅ Detecting user mood using AI (facial emotion recognition)  
✅ Allowing manual mood selection  
✅ Finding nearby places using OpenStreetMap data  
✅ Explaining *why* a place is recommended  
✅ Showing locations on an interactive live map  

---

## 🧠 Key Features

- 🎭 **AI Mood Detection** using DeepFace
- 😊 Manual Mood Selection Option
- 📍 Nearby Place Recommendation
- 🗺️ Interactive Map (React Leaflet)
- 💡 Explainable AI Recommendations
- 📏 Distance Calculation from User
- 🔄 API Failover System (Reliable Backend)
- 🎥 Optional Webcam Emotion Detection
- ⚡ Real-time Recommendations

---

## 🏗️ System Architecture
User → React Frontend → Flask API → AI Model + OpenStreetMap → Results → Map UI


### Flow:
1. User selects mood or uses webcam detection
2. Frontend sends mood + location to backend
3. Backend queries OpenStreetMap (Overpass API)
4. AI logic maps mood → place types
5. Results returned with explanation
6. Map & cards display recommendations

---

## 🛠️ Tech Stack

### Frontend
- React.js
- Axios
- React Leaflet
- HTML5 / CSS3

### Backend
- Python
- Flask
- Flask-CORS
- DeepFace (Emotion Recognition)
- OpenCV
- Requests API

### APIs & Data
- OpenStreetMap (Overpass API)
- Browser Geolocation API

---

## 📂 Project Structure
mood-places-recommender/
│
├── backend/
│ └── app.py
│
├── frontend/
│ └── src/
│ ├── App.js
│ ├── MapView.js
│ ├── EmotionDetector.js
│ ├── api.js
│ └── index.css
│
└── README.md


---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/Mood_Places_Recommender.git
cd Mood_Places_Recommender

### Backend
cd backend
python -m venv ai_env
ai_env\Scripts\activate
pip install flask flask-cors requests deepface opencv-python numpy
python app.py


### frontend
cd frontend
npm install
npm start