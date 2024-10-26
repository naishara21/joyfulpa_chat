# app.py
import os
import requests
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

# Set the model you want to use
API_URL = "https://api-inference.huggingface.co/models/gpt2"  # Example model, you can change it

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')

    headers = {
        "Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"  # Your Hugging Face API key
    }
    payload = {"inputs": user_message}

    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        bot_message = response.json()[0]['generated_text']
        return jsonify({'response': bot_message})
    else:
        return jsonify({'response': 'Error occurred while processing the request.'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
