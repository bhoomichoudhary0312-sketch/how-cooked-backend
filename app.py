from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import os

app = Flask(__name__)
CORS(app)

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

@app.route('/')
def home():
    return jsonify({
         "version": "NEW_BACKEND_V2"
    })

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    print("Received data:", data)

    diff_map = {
        "Easy": 1,
        "Medium": 2,
        "Hard": 3
    }

    difficulty_val = diff_map.get(
        data.get('difficulty', 'Medium'),
        2
    )

    attendance = float(data.get('attendance', 75))
    internal_marks = float(data.get('internalMarks', 15))
    assignments = float(data.get('assignments', 80))
    sleep = float(data.get('sleep', 6))
    study = float(data.get('study', 2))
    backlogs = int(data.get('backlogs', 0))

    cooked_score = (
    (100 - attendance) * 0.25 +
    (30 - internal_marks) * 0.80 +
    (100 - assignments) * 0.15 +
    backlogs * 8 +
    max(0, 7 - sleep) * 2 +
    max(0, 5 - study) * 3 +
    difficulty_val * 3
)

    cooked_percentage = round(
        min(max(cooked_score, 0), 100),
        1
    )

    if cooked_percentage >= 70:
        status = "Deep Fried"
    elif cooked_percentage >= 35:
        status = "Warning"
    else:
        status = "Safe"

    return jsonify({
        "cooked_percentage": cooked_percentage,
        "pass_probability": round(100 - cooked_percentage, 1),
        "roast": random.choice(ROAST_DATABASE[status]),
        "status": status + (
            " 💀" if status == "Deep Fried"
            else " ⚠️" if status == "Warning"
            else " 😎"
        )
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)