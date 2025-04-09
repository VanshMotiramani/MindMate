import joblib
import pandas as pd
import random
from textblob import TextBlob

# Load the model from the .pkl file
MODEL_PATH = "app/mental_health_model.pkl"
model = joblib.load(MODEL_PATH)

# Load songs dataset for music recommendation
songs_df = pd.read_csv("app/dataset.csv")  # Update path if needed

def analyze_emotions(text: str):
    """Analyze emotions using TextBlob."""
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    word_count = len(text.split())

    return {
        "sentiment": sentiment,
        "subjectivity": subjectivity,
        "depression_score": 1 if sentiment < -0.5 else 0,
        "anxiety_score": 1 if "anxious" in text.lower() else 0,
        "stress_score": 1 if "stressed" in text.lower() else 0,
        "is_crisis": sentiment < -0.7,
        "word_count": word_count
    }

def recommend_music(emotion):
    """Filter songs based on emotion."""
    emotion_keywords = {
        "happy": ["pop", "dance", "electronic"],
        "sad": ["blues", "acoustic", "soul"],
        "angry": ["metal", "rock", "rap"],
        "calm": ["ambient", "lofi", "chill"],
        "anxious": ["classical", "instrumental"],
        "normal": ["latin", "piano", "reggae"]
    }

    genre_tags = emotion_keywords.get(emotion.lower(), ["latin"])
    filtered = songs_df[songs_df['track_genre'].isin(genre_tags)]

    return filtered.sample(min(5, len(filtered)))[['track_name', 'artists', 'track_genre']].to_dict(orient='records')

def get_comprehensive_support(text: str):
    """Main function to get recommendation based on input."""
    prediction = model.predict([text])[0]  # e.g. Depression, Normal, etc.
    emotions = analyze_emotions(text)

    coping_mechanisms = {
        "Depression": [
            "Sleep hygiene", "Breathing exercise", "Walking or Nature Walks",
            "Read a book", "Go for a walk", "Hydration"
        ],
        "Anxiety": [
            "Mindfulness", "Talk to a friend", "Deep breathing", "Gratitude journaling"
        ],
        "Suicidal": [
            "Immediate help", "Crisis hotline", "Reach out to counselor", "Emergency support"
        ],
        "Normal": [
            "Keep journaling", "Meditation", "Healthy diet", "Stay connected"
        ]
    }

    return {
        "status": prediction,
        "emotions": emotions,
        "coping_mechanisms": coping_mechanisms.get(prediction, ["Take a break"]),
        "music": recommend_music(prediction)
    }
