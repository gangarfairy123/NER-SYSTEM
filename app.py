from flask import Flask, request, jsonify
import spacy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
nlp = spacy.load("model")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    text = data.get("text")

    doc = nlp(text)

    entities = []
    for ent in doc.ents:
        entities.append({
            "text": ent.text,
            "label": ent.label_
        })

    return jsonify({"entities": entities})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)