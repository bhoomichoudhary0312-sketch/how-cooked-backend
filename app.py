from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import random
import os

app = Flask(__name__)
CORS(app)

# 1. Load the trained AI model
try:
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    print("Error: model.pkl not found. Please run train_model.py first!")
    model = None

ROAST_DATABASE = {
    "Safe": [
        "You're actually doing okay. Stop overreacting, nerd.",
        "Living dangerously on the edge of success.",
        "Academic weapon in the making?",
        "Is it possible? A student with a functional sleep schedule?"
    ],
    "Warning": [
        "The library misses you. Go visit once in a while.",
        "Your GPA is currently on life support.",
        "Bro studies like WiFi signals in a basement—barely there.",
        "You're one bad quiz away from a villain origin story."
    ],
    "Deep Fried": [
        "It's not looking good, champ. Start learning how to flip burgers.",
        "Academic comeback not found. Error 404.",
        "You're not just cooked, you're incinerated. 💀",
        "Your transcript looks like a specialized menu at a BBQ joint."
    ]
}

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    
    # Mapping difficulty string to numbers (AI only understands numbers)
    diff_map = {"Easy": 1, "Medium": 2, "Hard": 3}
    difficulty_val = diff_map.get(data.get('difficulty', 'Medium'), 2)

    # Prepare the input for the model
    # Order must match the order in train_model.py
    features = np.array([[
        float(data.get('attendance', 75)),
        float(data.get('internalMarks', 15)),
        float(data.get('assignments', 80)),
        float(data.get('sleep', 6)),
        float(data.get('study', 2)),
        int(data.get('backlogs', 0)),
        difficulty_val
    ]])

    if model:
        # Use AI Model
        prediction_prob = model.predict_proba(features)[0][1] * 100
    else:
        # Fallback Logic (if AI is not available)
        score = (
            (100 - float(data.get('attendance', 75))) * 0.4 +
            (30 - float(data.get('internalMarks', 15))) * 1.5 +
            (int(data.get('backlogs', 0)) * 15)
        )
        prediction_prob = min(max(score, 0), 100)

    cooked_percentage = round(prediction_prob, 1)

    # Determine status and roast
    if cooked_percentage > 70:
        status = "Deep Fried"
    elif cooked_percentage > 35:
        status = "Warning"
    else:
        status = "Safe"

    return jsonify({
        "cooked_percentage": cooked_percentage,
        "pass_probability": round(100 - cooked_percentage, 1),
        "roast": random.choice(ROAST_DATABASE[status]),
        "status": status + (" 💀" if status == "Deep Fried" else " ⚠️" if status == "Warning" else " 😎")
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)