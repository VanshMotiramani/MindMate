import joblib
import os

model_path = os.path.join(os.path.dirname(__file__), "sentiment_model.pkl")
model = joblib.load(model_path)

def get_recommendation(text: str) -> str:
    try:
        pred = model.predict([text])[0]
        return pred
    except Exception as e:
        return "Could not process sentiment."