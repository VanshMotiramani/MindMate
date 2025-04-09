import joblib
import pandas as pd
from textblob import TextBlob

# Load trained model
model = joblib.load("app/mental_health_model.pkl")

# Load datasets (already preprocessed)
music_df = pd.read_csv("app/dataset.csv")  # Spotify track dataset
student_df = pd.read_csv("app/Student_Mental_Stress_and_Coping_Mechanisms.csv")  # Coping mechanisms

# Clean student dataset
student_df = student_df.dropna(subset=['Stress Coping Mechanisms', 'Mental Stress Level'])
student_df['Stress Category'] = student_df['Mental Stress Level'].apply(
    lambda x: 'High' if x >= 8 else 'Medium' if x >= 5 else 'Low'
)

# Clean music dataset
music_df = music_df.dropna(subset=['track_name', 'valence', 'energy'])

# Define feature ranges per mental health category
MUSIC_FEATURES = {
    'Depression': {'valence': (0.1, 0.4), 'energy': (0.2, 0.5)},
    'Anxiety': {'valence': (0.3, 0.6), 'energy': (0.2, 0.6)},
    'Stress': {'valence': (0.4, 0.6), 'energy': (0.3, 0.6)},
    'Suicidal': {'valence': (0.1, 0.3), 'energy': (0.2, 0.4)},
    'Bipolar': {'valence': (0.3, 0.7), 'energy': (0.3, 0.7)},
    'Personality Disorder': {'valence': (0.4, 0.7), 'energy': (0.4, 0.7)},
    'Normal': {'valence': (0.5, 0.9), 'energy': (0.5, 0.9)},
}

COPING_STRATEGIES = {
    "Normal": {"Low": ["Read a book", "Go for a walk"], "Medium": ["Talk to a friend"], "High": ["Yoga"]},
    "Depression": {
        "Low": ["Meditation", "Light exercise"],
        "Medium": ["Therapy session", "Talk to someone"],
        "High": ["Crisis helpline", "Breathing exercises"]
    },
    "Stress": {
        "Low": ["Break tasks", "Stretching"],
        "Medium": ["Journaling", "Time management"],
        "High": ["Breathing", "Nature walk"]
    },
    "Anxiety": {
        "Low": ["Positive affirmations"],
        "Medium": ["Relaxation audio", "Deep breathing"],
        "High": ["Grounding exercise", "Professional therapy"]
    },
    "Suicidal": {
        "Low": ["Call support line"],
        "Medium": ["Immediate help", "Therapist talk"],
        "High": ["Emergency contact", "Hospital visit"]
    },
    "Bipolar": {
        "Low": ["Routine", "Sleep hygiene"],
        "Medium": ["Mood tracking", "Consult psychiatrist"],
        "High": ["Therapy", "Medication check"]
    },
    "Personality Disorder": {
        "Low": ["Self-reflection", "Journaling"],
        "Medium": ["Mindfulness", "Peer support"],
        "High": ["Therapy", "Self-soothing"]
    },
}

# Emotion analysis
def analyze_emotions(text):
    analysis = TextBlob(text)
    words = text.lower().split()
    depression_words = ['depress', 'hopeless', 'empty', 'worthless']
    anxiety_words = ['anxious', 'panic', 'overwhelm', 'fear']
    stress_words = ['stress', 'pressure', 'burnout', 'exhaust']
    crisis_words = ['suicid', 'end it', 'kill myself', 'not want to live']

    return {
        'sentiment': analysis.sentiment.polarity,
        'subjectivity': analysis.sentiment.subjectivity,
        'depression_score': sum(word in w for w in words for word in depression_words),
        'anxiety_score': sum(word in w for w in words for word in anxiety_words),
        'stress_score': sum(word in w for w in words for word in stress_words),
        'is_crisis': any(word in text.lower() for word in crisis_words),
        'word_count': len(words)
    }

def get_coping_recommendations(status, emotional_features):
    stress_level = 'High' if emotional_features['is_crisis'] else ('Medium' if emotional_features['sentiment'] < -0.3 else 'Low')
    recommendations = COPING_STRATEGIES.get(status, COPING_STRATEGIES['Normal']).get(stress_level, []).copy()

    similar_students = student_df[student_df['Stress Category'] == stress_level]
    if not similar_students.empty:
        top_mechanisms = similar_students['Stress Coping Mechanisms'].value_counts().index[:3]
        recommendations.extend(top_mechanisms)

    recommendations.extend(["Hydration", "Sleep hygiene", "Breathing exercise"])
    return list(set(recommendations))[:8]

def get_music_recommendations(status, emotional_features):
    features = MUSIC_FEATURES.get(status, MUSIC_FEATURES['Normal'])
    valence_min = max(0.1, features['valence'][0] + emotional_features['sentiment'] * 0.1)
    valence_max = min(1.0, features['valence'][1] + emotional_features['sentiment'] * 0.1)

    query = f"(valence >= {valence_min}) & (valence <= {valence_max}) & (energy >= {features['energy'][0]}) & (energy <= {features['energy'][1]})"
    results = music_df.query(query)

    if results.shape[0] < 5:
        results = music_df.query(f"(valence >= {valence_min}) & (valence <= {valence_max})")

    return results.sort_values("popularity", ascending=False).head(5)

def get_comprehensive_support(text: str):
    try:
        status = model.predict([text])[0]
        emotions = analyze_emotions(text)
        coping = get_coping_recommendations(status, emotions)
        music = get_music_recommendations(status, emotions)

        return {
            "status": status,
            "emotions": emotions,
            "coping_mechanisms": coping,
            "music": music[['track_name', 'artists', 'track_genre']].to_dict(orient='records')
        }
    except Exception as e:
        return {
            "error": str(e),
            "fallback": [
                "Deep breathing exercise",
                "Reach out to a trusted person",
                "Consider professional help"
            ]
        }
