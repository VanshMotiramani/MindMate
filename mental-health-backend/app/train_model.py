import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.pipeline import Pipeline
import joblib

# Load data
df = pd.read_csv("Combined Data.csv")

# Drop rows with missing statements or status
df.dropna(subset=["statement", "status"], inplace=True)

# Reset index just to keep things clean
df.reset_index(drop=True, inplace=True)

X = df["statement"]
y = df["status"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build pipeline
model = Pipeline([
    ("tfidf", TfidfVectorizer(max_features=5000)),
    ("clf", LogisticRegression(max_iter=1000))
])

# Train model
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
conf = confusion_matrix(y_test, y_pred)

print(f"✅ Accuracy: {acc:.2f}")
print(f"📊 Confusion Matrix:\n{conf}")

# Save model
joblib.dump(model, "app/sentiment_model.pkl")
