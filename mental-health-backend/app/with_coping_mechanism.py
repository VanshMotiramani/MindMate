# # -*- coding: utf-8 -*-
# """with_coping_mechanism.ipynb

# Automatically generated by Colab.

# Original file is located at
#     https://colab.research.google.com/drive/1x1qyGkJ4mzcw6isJjDAnsIWxTzyJneuA
# """

# # ======================
# # 1. SETUP & INSTALLATIONS
# # ======================
# !pip install pandas scikit-learn joblib textblob
# !python -m textblob.download_corpora

# import pandas as pd
# import numpy as np
# import joblib
# from textblob import TextBlob
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.linear_model import LogisticRegression
# from sklearn.pipeline import Pipeline
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import classification_report
# from sklearn.utils.class_weight import compute_class_weight
# from google.colab import files
# import re
# import os
# import json
# from zipfile import ZipFile

# # ======================
# # 2. DATA LOADING
# # ======================
# from google.colab import files
# kaggle_dictionary = json.load(open("kaggle.json"))
# os.environ["KAGGLE_USERNAME"] = kaggle_dictionary["username"]
# os.environ["KAGGLE_KEY"] = kaggle_dictionary["key"]

# !kaggle datasets download -d suchintikasarkar/sentiment-analysis-for-mental-health
# !kaggle datasets download -d maharshipandya/-spotify-tracks-dataset
# !kaggle datasets download -d salahuddinahmedshuvo/student-mental-stress-and-coping-mechanisms

# with ZipFile("/content/sentiment-analysis-for-mental-health.zip", "r") as zip_ref:
#     zip_ref.extractall("/content")
# with ZipFile("/content/-spotify-tracks-dataset.zip", "r") as zip_ref:
#     zip_ref.extractall("/content")
# with ZipFile("/content/student-mental-stress-and-coping-mechanisms.zip", "r") as zip_ref:
#     zip_ref.extractall("/content")

# # Load datasets
# mh_df = pd.read_csv("Combined Data.csv")  # Mental health statements
# music_df = pd.read_csv("dataset.csv")     # Spotify tracks
# student_df = pd.read_csv("Student_Mental_Stress_and_Coping_Mechanisms.csv")  # Coping data

# # ======================
# # 3. DATA PREPROCESSING
# # ======================

# # Clean and standardize mental health data
# mh_df['status'] = mh_df['status'].str.replace('Bi-Polar', 'Bipolar')
# valid_statuses = ['Normal', 'Depression', 'Anxiety', 'Stress', 'Suicidal', 'Bipolar', 'Personality Disorder']
# mh_df = mh_df[mh_df['status'].isin(valid_statuses)].dropna(subset=['statement'])

# # Process student coping data - we'll use stress levels directly
# student_df = student_df.dropna(subset=['Stress Coping Mechanisms', 'Mental Stress Level'])
# student_df['Stress Category'] = student_df['Mental Stress Level'].apply(
#     lambda x: 'High' if x >= 8 else 'Medium' if x >= 5 else 'Low')

# # Clean music data
# music_df = music_df.dropna(subset=['track_name', 'valence', 'energy'])

# # ======================
# # 4. EMOTIONAL ANALYSIS ENGINE
# # ======================

# def analyze_emotions(text):
#     """Deep emotional feature extraction"""
#     analysis = TextBlob(text)
#     words = text.lower().split()

#     # Emotional dictionaries
#     depression_words = ['depress', 'hopeless', 'empty', 'worthless']
#     anxiety_words = ['anxious', 'panic', 'overwhelm', 'fear']
#     stress_words = ['stress', 'pressure', 'burnout', 'exhaust']
#     crisis_words = ['suicid', 'end it', 'kill myself', 'not want to live']

#     return {
#         'sentiment': analysis.sentiment.polarity,
#         'subjectivity': analysis.sentiment.subjectivity,
#         'depression_score': sum(word in w for w in words for word in depression_words),
#         'anxiety_score': sum(word in w for w in words for word in anxiety_words),
#         'stress_score': sum(word in w for w in words for word in stress_words),
#         'is_crisis': any(word in text.lower() for word in crisis_words),
#         'word_count': len(words)
#     }

# # ======================
# # 5. COMPREHENSIVE MAPPINGS
# # ======================

# COPING_STRATEGIES = {
#     'Depression': {
#         'Low': ["Gratitude journal", "Walk in nature", "Reach out to friend"],
#         'Medium': ["Behavioral activation", "Therapy appointment", "Small achievable goals"],
#         'High': ["Crisis hotline", "Safety plan", "Emergency contact"]
#     },
#     'Anxiety': {
#         'Low': ["Box breathing", "5-4-3-2-1 grounding"],
#         'Medium': ["Worry time limitation", "Progressive muscle relaxation"],
#         'High': ["Remove triggers", "Safe space", "Medication check"]
#     },
#     'Stress': {
#         'Low': ["Time management", "Prioritization"],
#         'Medium': ["Short breaks", "Nature walks"],
#         'High': ["Delegate tasks", "Learn to say no"]
#     },
#     'Suicidal': {
#         'Low': ["Safety plan", "Regular check-ins"],
#         'Medium': ["Remove means", "Stay with someone"],
#         'High': ["Immediate professional help", "Go to hospital"]
#     },
#     'Bipolar': {
#         'Low': ["Mood tracking", "Sleep schedule"],
#         'Medium': ["Routine establishment", "Symptom monitoring"],
#         'High': ["Therapist contact", "Medication review"]
#     },
#     'Personality Disorder': {
#         'Low': ["DBT skills", "Emotion regulation"],
#         'Medium': ["Distress tolerance", "Validation"],
#         'High': ["Crisis skills", "Support system"]
#     },
#     'Normal': {
#         'Low': ["Maintain routine", "Social activities"],
#         'Medium': ["Stress awareness", "Self-care"],
#         'High': ["Early intervention", "Preventive measures"]
#     }
# }

# MUSIC_FEATURES = {
#     'Depression': {
#         'valence': (0.6, 0.9),
#         'energy': (0.5, 0.8),
#         'tags': ['uplifting', 'hopeful', 'inspirational']
#     },
#     'Anxiety': {
#         'valence': (0.4, 0.7),
#         'energy': (0.3, 0.6),
#         'tags': ['calming', 'soothing', 'ambient']
#     },
#     'Stress': {
#         'valence': (0.5, 0.8),
#         'energy': (0.4, 0.7),
#         'tags': ['relaxing', 'peaceful', 'instrumental']
#     },
#     'Suicidal': {
#         'valence': (0.7, 0.95),
#         'energy': (0.7, 0.9),
#         'tags': ['energetic', 'positive', 'dance']
#     },
#     'Bipolar': {
#         'valence': (0.5, 0.8),
#         'energy': (0.5, 0.8),
#         'tags': ['balanced', 'stable', 'melodic']
#     },
#     'Personality Disorder': {
#         'valence': (0.5, 0.8),
#         'energy': (0.5, 0.8),
#         'tags': ['emotional', 'connecting', 'relational']
#     },
#     'Normal': {
#         'valence': (0.5, 0.9),
#         'energy': (0.5, 0.9),
#         'tags': ['enjoyable', 'pleasant', 'diverse']
#     }
# }

# # ======================
# # 6. MODEL TRAINING
# # ======================

# def train_mental_health_model():
#     X = mh_df['statement']
#     y = mh_df['status']

#     classes = np.unique(y)
#     weights = compute_class_weight('balanced', classes=classes, y=y)
#     class_weights = dict(zip(classes, weights))

#     model = Pipeline([
#         ('tfidf', TfidfVectorizer(
#             max_features=10000,
#             ngram_range=(1, 2),
#             stop_words='english',
#             min_df=3)),
#         ('clf', LogisticRegression(
#             max_iter=1000,
#             class_weight=class_weights,
#             solver='saga'))
#     ])

#     X_train, X_test, y_train, y_test = train_test_split(
#         X, y, test_size=0.2, random_state=42, stratify=y)

#     model.fit(X_train, y_train)

#     # Evaluation
#     y_pred = model.predict(X_test)
#     print("\nModel Evaluation:")
#     print(classification_report(y_test, y_pred))

#     return model

# # Load or train model
# try:
#     model = joblib.load("mental_health_model.pkl")
#     print("\nLoaded pre-trained model")
# except:
#     print("\nTraining new model...")
#     model = train_mental_health_model()
#     joblib.dump(model, "mental_health_model.pkl")

# # ======================
# # 7. PERSONALIZED RECOMMENDATION ENGINE
# # ======================

# def get_coping_recommendations(status, emotional_features):
#     """Get 5 unique, personalized coping strategies."""
#     # Determine stress level
#     if emotional_features['is_crisis']:
#         stress_level = 'High'
#     elif emotional_features['sentiment'] < -0.3:
#         stress_level = 'Medium'
#     else:
#         stress_level = 'Low'

#     # Base recommendations (from predefined mappings)
#     base_recs = COPING_STRATEGIES.get(status, COPING_STRATEGIES['Normal']).get(stress_level, []).copy()

#     # Add data-driven recommendations (from student dataset)
#     similar_students = student_df[
#         (student_df['Stress Category'] == stress_level)
#     ]
#     data_driven_recs = []
#     if not similar_students.empty:
#         top_mechanisms = similar_students['Stress Coping Mechanisms'].value_counts().index.tolist()
#         data_driven_recs = top_mechanisms[:3]  # Take top 3 from dataset

#     # Universal fallbacks (always included if space allows)
#     universal_recs = ["Hydration", "Sleep hygiene", "Breathing exercise"]

#     # Combine all, shuffle, and pick top 5 unique
#     all_recs = base_recs + data_driven_recs + universal_recs
#     unique_recs = list(set(all_recs))  # Remove duplicates
#     np.random.shuffle(unique_recs)     # Randomize order

#     return unique_recs[:5]  # Return 5 max

# def get_music_recommendations(status, emotional_features):
#     """Get emotion-matched music with varied recommendations"""
#     features = MUSIC_FEATURES.get(status, MUSIC_FEATURES['Normal'])

#     # Widen the valence/energy ranges
#     valence_min = max(0.1, features['valence'][0] - 0.2 + (emotional_features['sentiment'] * 0.1))
#     valence_max = min(1.0, features['valence'][1] + 0.2 + (emotional_features['sentiment'] * 0.1))
#     energy_min = max(0.1, features['energy'][0] - 0.1)
#     energy_max = min(1.0, features['energy'][1] + 0.1)

#     # Query music database with broader ranges
#     query = f"valence >= {valence_min} & valence <= {valence_max} & "
#     query += f"energy >= {energy_min} & energy <= {energy_max}"

#     results = music_df.query(query)

#     # If insufficient results, broaden further (ignore energy)
#     if len(results) < 20:
#         results = music_df.query(f"valence >= {valence_min} & valence <= {valence_max}")

#     # Randomly sample 5 songs from the top 50 (if available) to add variety
#     if len(results) > 5:
#         results = results.sort_values('popularity', ascending=False).head(50)
#         results = results.sample(n=5, random_state=42)
#     else:
#         results = results.head(5)

#     return results[['track_name', 'artists', 'track_genre']]

# def get_comprehensive_support(text):
#     """Full analysis pipeline"""
#     try:
#         # 1. Predict mental health status
#         status = model.predict([text])[0]

#         # 2. Deep emotional analysis
#         emotions = analyze_emotions(text)

#         # 3. Get personalized recommendations
#         coping = get_coping_recommendations(status, emotions)
#         music = get_music_recommendations(status, emotions)

#         return {
#             'input_text': text,
#             'mental_health_status': status,
#             'emotional_analysis': emotions,
#             'coping_mechanisms': coping,
#             'music_recommendations': music[['track_name', 'artists', 'track_genre']].to_dict('records')
#         }
#     except Exception as e:
#         return {
#             'error': str(e),
#             'input_text': text,
#             'fallback_recommendations': [
#                 "Deep breathing exercise",
#                 "Reach out to trusted friend/family",
#                 "Professional help if needed"
#             ]
#         }

# # ======================
# # 8. TESTING & DEMONSTRATION
# # ======================

# test_cases = [
#     "I feel completely worthless and empty inside",
#     "My heart is racing and I can't stop worrying about everything",
#     "The stress from work is making me physically ill",
#     "I have a plan to end my life tonight",
#     "My moods swing from extreme happiness to deep depression",
#     "I struggle with intense emotions in relationships",
#     "I'm feeling completely normal and balanced today"
# ]

# print("\nTesting Personalized Recommendations:")
# for text in test_cases:
#     result = get_comprehensive_support(text)

#     print("\n" + "="*80)
#     print(f"INPUT: {text}")

#     if 'error' in result:
#         print(f"ERROR: {result['error']}")
#         print("\nFALLBACK RECOMMENDATIONS:")
#         for i, item in enumerate(result['fallback_recommendations'], 1):
#             print(f"{i}. {item}")
#         continue

#     print(f"PREDICTED STATUS: {result['mental_health_status']}")
#     print(f"EMOTIONAL ANALYSIS: Sentiment={result['emotional_analysis']['sentiment']:.2f}, Crisis={result['emotional_analysis']['is_crisis']}")

#     print("\nRECOMMENDED COPING MECHANISMS:")
#     for i, item in enumerate(result['coping_mechanisms'], 1):
#         print(f"{i}. {item}")

#     print("\nRECOMMENDED MUSIC:")
#     for song in result['music_recommendations']:
#         print(f"- {song['track_name']} by {song['artists']} ({song['track_genre']})")

# # ======================
# # 9. SAVE MODEL (Optional)
# # ======================
# files.download('mental_health_model.pkl')