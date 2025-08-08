# sentiment.py

import os
import requests

HUGGINGFACE_API_TOKEN = os.environ.get("HUGGINGFACE_API_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"

def query_sentiment_api(payload):
    """Sends a request to the Hugging Face Inference API."""
    if not HUGGINGFACE_API_TOKEN:
        print("Hugging Face API token not found.")
        return None
        
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def detect_mood(text: str) -> str:
    """
    Analyzes the sentiment of the text using the Hugging Face API.
    """
    chill_keywords = ["bored", "calm", "relaxed", "nothing", "meh", "okay", "alright", "fine"]
    if any(keyword in text.lower() for keyword in chill_keywords):
        return "chill"

    try:
        output = query_sentiment_api({"inputs": text})
        
        if output and isinstance(output, list) and output[0]:
            label = output[0][0]['label']
            
            if label == "POSITIVE":
                return "happy"
            else: # NEGATIVE
                return "mellow"
        
        return "chill"

    except Exception as e:
        print(f"Error during Hugging Face API call: {e}")
        return "mellow"
