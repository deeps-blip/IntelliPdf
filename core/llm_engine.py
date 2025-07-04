# core/llm_engine.py

import os
import requests
from dotenv import load_dotenv

# Load your Google API Key from .env file
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

def call_gemini(prompt):
    if not API_KEY:
        return "❌ Gemini API key not found. Please set GOOGLE_API_KEY in your .env file."

    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
    "contents": [{"parts": [{"text": prompt}]}],
    "generationConfig": {
        "maxOutputTokens": 300  # Limit response length
    }
}

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"❌ Gemini API Error {response.status_code}: {response.text}"
    except requests.exceptions.RequestException as e:
        return f"❌ Network error while contacting Gemini API: {str(e)}"
