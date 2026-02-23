# 🌍 AI Mood-Based Intelligent Travel Recommender

An AI-powered location-aware recommendation system that suggests nearby places based on user mood using NLP sentiment analysis, semantic embeddings, and self-learning personalization.

---

## 🚀 Live Demo

Frontend: https://YOUR-VERCEL-LINK  
Backend API: https://mood-places-recommender.onrender.com

---

## 🧠 Project Overview

This project builds an intelligent recommendation engine that understands user emotions through text or voice input and recommends nearby locations dynamically.

Unlike traditional rule-based systems, this application uses:

- NLP sentiment analysis
- Semantic similarity embeddings
- Location-based search
- Online learning from user feedback

to continuously improve recommendations.

---

## ✨ Features

✅ Mood detection using NLP (TextBlob)  
✅ Voice-based emotion input (Web Speech API)  
✅ Location-aware recommendations  
✅ Intelligent ranking using sentence embeddings  
✅ Self-learning personalization system  
✅ Real-time nearby place discovery (OpenStreetMap API)  
✅ Backend warmup detection for cloud deployment  
✅ Fully deployed cloud application

---

## 🧱 Tech Stack

### Frontend
- React.js
- Tailwind CSS
- Axios

### Backend
- FastAPI
- Python

### AI / ML
- Sentence Transformers
- Semantic Similarity Ranking
- NLP Sentiment Analysis

### APIs
- OpenStreetMap Overpass API
- Google Maps Links

### Deployment
- Render (Backend)
- Vercel (Frontend)

---

## ⚙️ System Architecture
User (Voice/Text Mood)
↓
NLP Sentiment Detection
↓
User Location (GPS)
↓
Nearby Places API
↓
Sentence Embedding Model
↓
Similarity Scoring
↓
Learning Feedback Engine
↓
Personalized Recommendations

---

## 🧩 How It Works

1. User provides mood via text or voice.
2. NLP analyzes emotional polarity.
3. User location fetches nearby places.
4. AI embeddings compare mood meaning with place categories.
5. Recommendations are ranked by semantic similarity.
6. User interactions are stored as feedback.
7. Future results improve automatically.

---

## 🖥️ Run Locally

### Backend

```bash
cd backend
.\venv\Scripts\activate
python -m uvicorn app:app --reload