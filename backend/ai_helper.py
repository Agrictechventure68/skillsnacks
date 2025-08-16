import openai, os
import time
openai.api_key = os.getenv("OPENAI_API_KEY")

def explain_topic(topic):
    prompt = f"Explain {topic} in a simple and friendly way for a beginner hustler."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']



    last_request_time = 0
    MIN_INTERVAL = 2  # seconds

    def get_ai_response(prompt):
        global last_request_time
        now = time.time()
        if now - last_request_time < MIN_INTERVAL:
            time.sleep(MIN_INTERVAL - (now - last_request_time))
        try:
            last_request_time = time.time()
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=150
            )
            return response.choices[0].text.strip()
        except Exception as e:
            print(f"Error with OpenAI API: {e}")
            return "Sorry, I'm having trouble processing that request right now."