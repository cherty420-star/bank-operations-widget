import os
import requests
from dotenv import load_dotenv

load_dotenv('.env')

API_KEY = os.getenv('EXCHANGE_RATE_API_KEY')
print(f"API Key: {API_KEY}")

# Тестируем API
headers = {"apikey": API_KEY}
url = "https://api.apilayer.com/exchangerates_data/latest?base=USD&symbols=RUB"

try:
    response = requests.get(url, headers=headers, timeout=10)
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print("API Response:", data)
        usd_to_rub = data['rates']['RUB']
        print(f"1 USD = {usd_to_rub} RUB")
    else:
        print(f"Error: {response.status_code} - {response.text}")

except Exception as e:
    print(f"API Error: {e}")