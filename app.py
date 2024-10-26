import os
import requests
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from flask_cors import CORS  # Import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

RASA_API_URL = "http://localhost:5005/webhooks/rest/webhook"  # Rasa API endpoint
RASA_API_KEY = os.getenv('RASA_API_KEY')  # Load the API key from .env

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send-message', methods=['POST'])
def send_message():
    user_message = request.form.get('message')

    headers = {
        'Authorization': f'Bearer {RASA_API_KEY}',
        'Content-Type': 'application/json'
    }

    payload = {
        "sender": "user",
        "message": user_message
    }

    response = requests.post(RASA_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        bot_message = response.json()
        return jsonify({'status': 'success', 'response': bot_message})
    else:
        return jsonify({'status': 'error', 'message': 'Error communicating with Rasa.'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=True)
