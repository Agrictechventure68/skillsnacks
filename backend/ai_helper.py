import openai, os
openai.api_key = os.getenv("OPENAI_API_KEY")

def explain_topic(topic):
    prompt = f"Explain {topic} in a simple and friendly way for a beginner hustler."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']



