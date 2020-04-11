import json
import requests
import concurrent.futures
from model.stock import Stock

# API Token and headers
TOKEN = "pk_179782678501460184c8f015057c382a"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0"}
MAX_WORKER = 10

# Hardcoded lists of token
# TODO persistent sotrage
SYMBOLS = {"AAPL", "ATVI", "BASFY", "FDX", "NFLX", "NVAX", "PCELF", "SAP", "PSMMF", "SYIEF"}


def get_stock(symbol: str) -> Stock:
    """
    Get values of the stock for the specified symbol.

    :param symbol: Symbol representing a stock.
    :return: Instance of a stock object
    """
    response = requests.get(f"https://cloud.iexapis.com/stable/stock/{symbol}/quote?token={TOKEN}", headers=HEADERS)

    def creator(obj) -> Stock:
        return Stock(obj["companyName"], symbol, obj["previousClose"],
                     obj["latestPrice"], obj["change"], obj["changePercent"])

    return json.loads(response.text, object_hook=creator)


if __name__ == '__main__':
    results = []

    # Start the executer with MAX_WORKER workers
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
        # Call get_stock for every symbol and store futures
        future_stock = {executor.submit(get_stock, symbol): symbol for symbol in SYMBOLS}
        # Iterate over each future when all are completed, add them to stocks list
        stocks = []
        for future in concurrent.futures.as_completed(future_stock):
            try:
                stock = future.result()
                stocks.append(stock)
            except Exception as exc:
                print('%r generated an exception: %s')

    print(*stocks, sep="\n")

