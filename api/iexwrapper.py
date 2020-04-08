import json
import requests

# API Token
TOKEN = "pk_179782678501460184c8f015057c382a"
SYMBOL = "AAPL"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0"}

if __name__ == '__main__':
    first_name = "Stafen"
    response = requests.get(f"https://cloud.iexapis.com/stable/stock/{SYMBOL}/quote?token={TOKEN}", headers=HEADERS)
    data = json.loads(response.text)

    for attr in data:
        value = data[attr]
        print(f"{attr} : {value}")
