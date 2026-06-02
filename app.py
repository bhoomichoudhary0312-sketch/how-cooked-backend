from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import os

app = Flask(__name__)
CORS(app)

ROAST_DATABASE = {
    "Academic Weapon 🏆": [
        "The topper is scared of YOU.",
        "Attendance up. Marks up. Life together. Suspicious.",
        "You're carrying the class average single-handedly.",
        "Touching grass and passing exams. Impressive."
    ],

    "Surviving 😎": [
        "Not perfect, but definitely not doomed.",
        "You're balancing chaos surprisingly well.",
        "One energy drink away from greatness.",
        "Still standing. That's what matters."
    ],

    "Slightly Cooked 🍳": [
        "The pan is heating up.",
        "You should probably start studying soon.",
        "Academic danger detected, but manageable.",
        "You're cooking... but not burnt yet."
    ],

    "Warning ⚠️": [
        "The library misses you.",
        "Your GPA is sending distress signals.",
        "One bad exam away from trouble.",
        "Time to stop saying 'I'll study tomorrow'."
    ],

    "Deep Fried 💀": [
        "Academic comeback not found. Error 404.",
        "Your transcript belongs in a museum.",
        "You're not cooked. You're charcoal.",
        "Even the syllabus has given up."
    ]
}

@app.route('/')
def home():
    return jsonify({
         "message": "How Cooked Are You Backend Running",
    "version": "2.0",
    "status": "success"
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

    attendance = max(0, min(100, float(data.get('attendance', 75))))
    internal_marks = max(0, min(30, float(data.get('internalMarks', 15))))
    assignments = max(0, min(100, float(data.get('assignments', 80))))
    sleep = max(0, min(24, float(data.get('sleep', 6))))
    study = max(0, min(24, float(data.get('study', 2))))
    backlogs = max(0, int(data.get('backlogs', 0)))

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

    if cooked_percentage >= 81:
        status = "Deep Fried 💀"
        recommendation = "Cancel distractions. Study immediately."

    elif cooked_percentage >= 61:
        status = "Warning ⚠️"
        recommendation = "Focus on weak subjects and increase study hours."

    elif cooked_percentage >= 41:
        status = "Slightly Cooked 🍳"
        recommendation = "A little more consistency can improve your score."

    elif cooked_percentage >= 21:
        status = "Surviving 😎"
        recommendation = "You're doing okay. Keep the momentum going."

    else:
        status = "Academic Weapon 🏆"
        recommendation = "Excellent work. Maintain your routine."
    return jsonify({
        "cooked_percentage": cooked_percentage,
        "pass_probability": round(100 - cooked_percentage, 1),
        "roast": random.choice(ROAST_DATABASE[status]),
        "status": status,
        "recommendation": recommendation
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)