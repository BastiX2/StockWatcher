import json
from termcolor import colored
import requests
import concurrent.futures
from model.stock import Stock

# API Token and headers
TOKEN = "pk_179782678501460184c8f015057c382a"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0"}
FILE = "data.txt"
MAX_WORKER = 10


def get_stock(name: str, symbol: str) -> Stock:
    """
    Get values of the stock for the specified symbol.

    :param name: Name of the stock
    :param symbol: Symbol representing a stock.
    :return: Instance of a stock object
    """
    response = requests.get(f"https://cloud.iexapis.com/stable/stock/{symbol}/quote?token={TOKEN}", headers=HEADERS)

    def creator(obj) -> Stock:
        return Stock(name, symbol, obj["previousClose"],
                     obj["latestPrice"], obj["change"], obj["changePercent"])

    if response.status_code == 200:
        return json.loads(response.text, object_hook=creator)

    print(colored(f"ERROR: No stock found for: {name}({symbol})", "red"))


def save_stocks(symbols: dict):
    """
    Save current stocks to file

    :param symbols: Dict of symbols to save to file.
    """
    data = json.dumps(symbols)
    with open(FILE, "w") as file:
        file.write(data)


def load_stocks() -> dict:
    """
    Read current stocks from file

    :return: Dict of stocks, empty dict if no file exist
    """
    stocks = {}
    with open(FILE, "r") as file:
        data = file.read()
        if data:
            stocks = json.loads(data)
    return stocks


def add_stock(name: str, symbol: str):
    """
    Add a new Stock to the file
    :param name:
    :param symbol:
    """
    stocks = load_stocks()
    stocks.update({name: symbol})
    save_stocks(stocks)


def delete_stock(symbol: str):
    """
    Remove the stock with the specified symbol.

    :param symbol: Symbol representing a stock
    """

    stocks = load_stocks()
    if symbol in stocks:
        del stocks[symbol]
        save_stocks(stocks)


def main():
    # Get symbols from file
    symbols = load_stocks()
    stocks = []
    # Start the executer with MAX_WORKER workers
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
        # Call get_stock for every symbol and store futures
        future_stock = {executor.submit(get_stock, name, symbol): symbol for symbol, name in symbols.items()}
        # Iterate over each future when all are completed, add them to stocks list

        for future in concurrent.futures.as_completed(future_stock):
            try:
                stock = future.result()
                if stock is not None:
                    stocks.append(stock)
            except Exception as ex:
                print('%r generated an exception: %s', ex)

    stocks.sort(key=lambda x: x.name)
    print(*stocks, sep="\n")
    print()


if __name__ == '__main__':
    main()
