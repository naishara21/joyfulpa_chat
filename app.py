# app.py
import os
from flask import Flask, request, jsonify, render_template
import openai
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")  # Use the environment variable for the API key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": user_message}
        ]
    )
    bot_message = response['choices'][0]['message']['content']
    return jsonify({'response': bot_message})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000)))
