import requests
import time

def fetch_stock_data(symbol, start_time, end_time, retries=3, delay=5):
    # Yahoo Finance API URL
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?period1={start_time}&period2={end_time}&interval=1d&lang=en-US&region=US"
    
    # Headers to mimic a browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    for attempt in range(retries):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            print(f"Rate limit reached. Retrying in {delay} seconds...")
            time.sleep(delay)
            delay *= 2  # Exponential backoff
        else:
            raise Exception(f"Failed to fetch data: {response.status_code}")

    raise Exception("Max retries exceeded. Could not fetch data.")