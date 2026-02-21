import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# Sample training data
data = {
    "text": [
        "I love this",
        "This is amazing",
        "Very happy today",
        "I hate this",
        "This is terrible",
        "Very bad experience"
    ],
    "sentiment": [
        "Positive",
        "Positive",
        "Positive",
        "Negative",
        "Negative",
        "Negative"
    ]
}

df = pd.DataFrame(data)

# Create pipeline
model = Pipeline([
    ("vectorizer", CountVectorizer()),
    ("classifier", LogisticRegression())
])

model.fit(df["text"], df["sentiment"])

# Save model
pickle.dump(model, open("model.pkl", "wb"))

print("Model trained and saved successfully!")