import os
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from module_loader import list_module_files, load_module_by_name, load_all_modules
from ai_helper import explain_topic

app = Flask(_name_)
# CORS: allow all for MVP; later restrict to your Vercel domain
CORS(app, resources={r"/": {"origins": ""}})

# --- Paths (supports contents/ at repo root) ---
BACKEND_DIR = os.path.dirname(os.path.abspath(_file_))
PROJECT_ROOT = os.path.abspath(os.path.join(BACKEND_DIR, ".."))
CONTENTS_DIR = os.path.join(PROJECT_ROOT, "contents")
QUIZ_FOLDER = os.path.join(CONTENTS_DIR, "quizzes")
os.makedirs(QUIZ_FOLDER, exist_ok=True)

# ---------- Health ----------
@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "skillsnacks-backend"})

# ---------- Skills (modules) ----------
@app.get("/api/skills")
def list_skills():
    """
    Returns a list of available module filenames (without .json) and optionally
    full data if ?full=1
    """
    full = request.args.get("full") in ("1", "true", "yes")
    files = list_module_files()
    if not full:
        return jsonify({"skills": files})
    modules = load_all_modules()
    return jsonify({"skills": modules})

@app.get("/api/skills/<skill_name>")
def get_skill(skill_name: str):
    """
    Return a single skill module by <skill_name> (filename without .json).
    """
    data = load_module_by_name(skill_name)
    if data is None:
        return jsonify({"error": "Skill not found"}), 404
    return jsonify(data)

# ---------- Quizzes ----------
@app.get("/api/quizzes/<quiz_name>")
def get_quiz(quiz_name: str):
    """
    Return a quiz JSON by filename (without .json) from contents/quizzes.
    """
    file_path = os.path.join(QUIZ_FOLDER, f"{quiz_name}.json")
    if not os.path.exists(file_path):
        return jsonify({"error": "Quiz not found"}), 404
    with open(file_path, "r", encoding="utf-8") as f:
        return jsonify(json.load(f))

# ---------- AI helper ----------
@app.post("/api/explain")
def api_explain():
    """
    Body: { "topic": "basic phone repair" }
    Returns an AI-generated explanation or safe fallback if AI key missing.
    """
    payload = request.get_json(silent=True) or {}
    topic = (payload.get("topic") or "").strip()
    if not topic:
        return jsonify({"error": "topic is required"}), 400
    app.logger.info(f"Explain requested for topic: {topic}")
    text = explain_topic(topic)
    return jsonify({"topic": topic, "explanation": text})

# ---------- Root ----------
@app.get("/")
def root():
    return jsonify({
        "message": "SkillSnacks backend is running",
        "docs": ["/health", "/api/skills", "/api/skills/<name>", "/api/quizzes/<name>", "/api/explain"]
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_DEBUG") == "1")