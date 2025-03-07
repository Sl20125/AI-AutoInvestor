import os
from dotenv import load_dotenv
import requests
import json

load_dotenv("../.env")

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def get_stock_price(symbol):
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}'
    response = requests.get(url)
    return response.json()

def get_latest_news(symbol):
    url = f'https://newsapi.org/v2/everything?q={symbol}&apiKey={NEWS_API_KEY}'
    response = requests.get(url)
    return response.json()

if __name__ == "__main__":
    symbol = "AAPL"

    print("🟢 Цена акции (AAPL):")
    price_data = get_stock_price(symbol)
    print(json.dumps(price_data, indent=4))

    print("\n🟢 Последние новости по AAPL:")
    news_data = get_latest_news(symbol)
    print(json.dumps(news_data, indent=2))
