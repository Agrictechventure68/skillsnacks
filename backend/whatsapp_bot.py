from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(_name_)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    """
    Handle incoming WhatsApp messages and send a response.
    """
    incoming_msg = request.values.get("Body", "").lower()
    response = MessagingResponse()

    if "hello" in incoming_msg:
        response.message("👋 Hi there! Welcome to SkillSnacks. How can we help you today?")
    elif "help" in incoming_msg:
        response.message("💡 You can ask about courses, resources, or say 'hello' to start.")
    else:
        response.message("✅ Thanks for reaching out! A SkillSnacks team member will get back to you soon.")

    return str(response)

if _name_ == "_main_":
    # Run locally on port 5000
    app.run(host="0.0.0.0", port=5000, debug=True)

