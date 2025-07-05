
# backend/whatsapp_bot.py
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from ai_helper import explain_topic

app = Flask(__name__)

@app.route("/bot", methods=['POST'])
def bot():
    msg = request.form.get('Body', '').strip().lower()
    response = MessagingResponse()
    reply = response.message

    if "start" in msg:
        reply.body("Welcome to SkillSnacks! Choose a topic:\na) Digital Skills\nb) Business Basics\nc) Hustler Tips")
    elif "explain" in msg:
        reply.body(explain_topic("Today's topic"))
    elif "quiz" in msg:
        reply.body("Quiz:\n1. What is digital marketing?\na) ...\nb) ...\nReply with 1a, 1b, etc.")
    elif "progress" in msg:
        reply.body("Your progress: (feature coming soon!)")
    else:
        reply.body("Reply 'Start' to begin or 'Explain' for help.")
    return str(response)
if __name__ == "__main__":
    app.run(debug=True)
    return str(response)

