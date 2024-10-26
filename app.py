# app.py
import os
import requests
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

# Set the model you want to use (GPT-Neo)
API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-2.7B"  # Change to GPT-Neo

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')

    headers = {
        "Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"  # Your Hugging Face API key
    }
    
    # Include context for better responses
    payload = {
        "inputs": f"User: {user_message}\nBot:",  # Provide context for the model
        "parameters": {
            "max_length": 50,  # Limit the response length
            "num_return_sequences": 1,
            "temperature": 0.7  # Adjust randomness
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        # Extract and clean the bot's response
        bot_message = response.json()[0]['generated_text'].split('Bot: ')[-1].strip()
        return jsonify({'response': bot_message})
    else:
        return jsonify({'response': 'Error occurred while processing the request.'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
