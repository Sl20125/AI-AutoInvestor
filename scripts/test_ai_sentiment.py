import os
import requests
from dotenv import load_dotenv
import json

# Обязательно правильно укажи путь!
load_dotenv("../.env")

HF_API_TOKEN = os.getenv("HF_API_KEY")

def sentiment_analysis(text):
    API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    response = requests.post(API_URL, headers=headers, json={"inputs": text})
    return response.json()

if __name__ == "__main__":
    text = "Apple stocks soared today after fantastic quarterly results announcement."
    sentiment = sentiment_analysis(text)
    print("Sentiment-анализ новости об Apple:", json.dumps(sentiment, indent=2))
