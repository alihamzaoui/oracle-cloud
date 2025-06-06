# app.py
from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI
import os

# The API Key will be set as a "Secret File" or environment variable on the cloud platform.
# This is the most secure method.
try:
    with open('/etc/secrets/openrouter_api_key', 'r') as f:
        API_KEY = f.read().strip()
except IOError:
    # Fallback for local testing if you still want to use a .env file
    from dotenv import load_dotenv
    load_dotenv()
    API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    raise ValueError("API key not found. Ensure you set it in the cloud environment.")

app = Flask(__name__, static_folder='static', static_url_path='')

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
)

@app.route('/ask_oracle', methods=['POST'])
def ask_oracle():
    data = request.json
    try:
        completion = client.chat.completions.create(
            model=data.get('model'),
            messages=[
                {"role": "system", "content": data.get('system_prompt')},
                {"role": "user", "content": data.get('prompt')},
            ],
        )
        return jsonify({"response": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
