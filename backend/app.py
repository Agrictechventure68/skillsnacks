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

