from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

@app.route('/generate', methods=['POST'])
def generate():
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        return jsonify({'error': 'API key not configured'}), 500

    data = request.get_json()
    prompt = data.get('prompt', '')

    try:
        res = requests.post(
            f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}',
            json={
                'contents': [{'parts': [{'text': prompt}]}],
                'generationConfig': {'maxOutputTokens': 3000}
            }
        )
        return jsonify(res.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
