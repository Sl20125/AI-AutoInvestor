import os
import requests
from dotenv import load_dotenv
import json

load_dotenv("../.env")

# Загрузка API-ключей
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
HF_API_TOKEN = os.getenv("HF_API_KEY")

# Получение текущей цены акции
def get_stock_price(symbol):
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}'
    response = requests.get(url).json()
    return response.get("Global Quote", {})

# Получение последних новостей по акции
def get_latest_news(symbol):
    url = f'https://newsapi.org/v2/everything?q={symbol}&apiKey={NEWS_API_KEY}&language=en'
    response = requests.get(url).json()
    return response.get("articles", [])[:5]

# Анализ настроения новостей с Hugging Face
def analyze_sentiment(text):
    url = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    response = requests.post(url, headers=headers, json={"inputs": text})
    result = response.json()

    # Берём sentiment с наибольшей вероятностью
    if isinstance(result, list) and len(result) > 0:
        best_sentiment = max(result[0], key=lambda x: x["score"])
        return best_sentiment
    return {"label": "NEUTRAL", "score": 0}

# Логика принятия инвестиционного решения
def make_investment_decision(sentiments):
    positive_count = sum(1 for s in sentiments if s["label"] == "POSITIVE")
    negative_count = sum(1 for s in sentiments if s["label"] == "NEGATIVE")

    if positive_count > negative_count:
        return "ПОКУПАТЬ"
    elif negative_count > positive_count:
        return "ПРОДАВАТЬ"
    else:
        return "ДЕРЖАТЬ"

# Главная логика работы программы
if __name__ == "__main__":
    symbol = "AAPL"
    
    print("📌 Получаем цену акции...")
    price_data = get_stock_price(symbol)
    print(json.dumps(price_data, indent=2))
    
    print("\n📌 Получаем последние новости...")
    news_articles = get_latest_news(symbol)
    
    sentiments = []
    for article in news_articles:
        sentiment = analyze_sentiment(article["title"])
        sentiments.append(sentiment)
        print(f"Новость: {article['title']}")
        print(f"Sentiment: {sentiment}\n")
    
    decision = make_investment_decision(sentiments)
    print(f"🤖 Решение AI-инвестора для акции {symbol}: {decision}")
