from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)

# Load trained sentiment model
model = pickle.load(open("model.pkl", "rb"))


@app.route("/")
def home():
    return jsonify({
        "message": "🚀 Sentiment Analysis API is running!"
    })


@app.route("/predict", methods=["POST"])
def predict():

    # ---- SAFE JSON FETCH ----
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({
            "error": "❌ Please provide text in JSON format."
        }), 400

    text = data["text"]

    # ---- LIMIT CHECK (50 characters) ----
    if len(text) > 50:
        return jsonify({
            "error": "⚠️ Text exceeds 50 character limit."
        }), 400

    # ---- SENTIMENT ----
    prediction = model.predict([text])[0]

    # ---- TEMPORARY Sarcasm + Emotion ----
    sarcasm = "No"
    emotion = "Neutral"

    lower_text = text.lower()

    # Emotion rules
    if "sad" in lower_text:
        emotion = "Sad"
    elif "happy" in lower_text:
        emotion = "Happy"
    elif "angry" in lower_text:
        emotion = "Angry"
    elif "love" in lower_text:
        emotion = "Happy"
    elif "hate" in lower_text:
        emotion = "Angry"

    # Sarcasm rule
    if "yeah right" in lower_text or "sure" in lower_text:
        sarcasm = "Yes"

    # ---- EMOJI MAPPING ----
    sentiment_emojis = {
        "positive": "😊",
        "negative": "😡",
        "neutral": "😐",
        "pos": "😊",
        "neg": "😡",
        "neu": "😐"
    }

    sarcasm_emojis = {
        "Yes": "🙃",
        "No": "❌"
    }

    emotion_emojis = {
        "Happy": "😄",
        "Sad": "😢",
        "Angry": "😠",
        "Neutral": "😐"
    }

    sentiment_emoji = sentiment_emojis.get(str(prediction).lower(), "🤖")
    sarcasm_emoji = sarcasm_emojis.get(sarcasm, "🤖")
    emotion_emoji = emotion_emojis.get(emotion, "🤖")

    return jsonify({
        "sentiment": prediction,
        "sentiment_emoji": sentiment_emoji,
        "sarcasm": sarcasm,
        "sarcasm_emoji": sarcasm_emoji,
        "emotion": emotion,
        "emotion_emoji": emotion_emoji
    })


if __name__ == "__main__":
    app.run(port=5000, debug=True)