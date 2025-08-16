from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/bot", methods=["POST"])
def bot_webhook():
    data = request.get_json()
    print(data)
    return jsonify({"message": "Received!"})

@app.route("/")
def home():
    return "SkillSnacks is working!"

if __name__ == "__main__":
    app.run(debug=True)

{
  "title": "Catering Basics",
  "category": "Food & Catering",
  "introduction": "...",
  "materials": ["Gas stove", "Pots", "Ingredients"],
  "steps": ["Step 1...", "Step 2..."],
  "tips": "...",
  "assessment": "..."
}
from flask import Flask, jsonify
import os, json

app = Flask(_name_)

QUIZ_FOLDER = "contents/quizzes"

@app.route('/api/skills/<skill_name>', methods=['GET'])
def get_skill_data(skill_name):
    file_path = os.path.join(QUIZ_FOLDER, f"{skill_name}.json")
    if not os.path.exists(file_path):
        return jsonify({"error": "Skill not found"}), 404

    with open(file_path, 'r') as f:
        data = json.load(f)
    return jsonify(data)

from flask import Flask, jsonify, send_from_directory
import os, json

app = Flask(_name_)
QUIZ_FOLDER = "contents/quizzes"

@app.route('/api/skills/<skill_name>')
def get_skill_data(skill_name):
    file_path = os.path.join(QUIZ_FOLDER, f"{skill_name}.json")
    if not os.path.exists(file_path):
        return jsonify({"error": "Skill not found"}), 404
    with open(file_path, 'r') as f:
        return jsonify(json.load(f))

@app.route('/')
def serve_index():
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('frontend', path)

if _name_ == '_main_':
    app.run(debug=True)

