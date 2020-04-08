import json
import requests

# API Token
TOKEN = "pk_179782678501460184c8f015057c382a"
SYMBOLS = {"AAPL", "ATVI", "BASFY", "FDX", "NFLX", "NVAX", "PCELF", "SAP", "PSMMF", "SYIEF"}
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0"}

if __name__ == '__main__':
    results = []
    for symbol in SYMBOLS:
        response = requests.get(f"https://cloud.iexapis.com/stable/stock/{symbol}/quote?token={TOKEN}", headers=HEADERS)
        data = json.loads(response.text)
        results.append(data)

    # Print to console
    header = '{:>25} {:>15} {:>15}  {:>10}'.format("name", "Close", "Current", "Change")
    print(header)
    for stock in results:
        current_value = stock["latestPrice"]
        old_value = stock["previousClose"]
        name = stock["companyName"]
        change = stock["change"]
        change_percent = stock["changePercent"]
        output = '{:>25} {:>15} {:>15}  {:>10}'.format(name,  old_value, current_value, change)
        print(output)
