import concurrent.futures
import json
from operator import attrgetter

import requests
from termcolor import colored

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


def save_stocks(symbols: dict, file_path: str):
    """
    Save current stocks to file

    :param file_path: File path to save the current stocks
    :param symbols: Dict of symbols to save to file.
    """
    data = json.dumps(symbols)
    with open(file_path, "w") as file:
        file.write(data)


def load_stocks(file_path: str) -> dict:
    """
    Read current stocks from file

    :param file_path: Path of the file to load stocks from
    :return: Dict of stocks, empty dict if no file exist
    """
    stocks = {}
    with open(file_path, "r") as file:
        data = file.read()
        if data:
            stocks = json.loads(data)
    return stocks


def add_stock(name: str, symbol: str, file_path: str):
    """
    Add a new Stock to the file

    :param name: name of the stock
    :param symbol: Symbol of the stock
    :param file_path: Path of the data file
    """
    stocks = load_stocks(file_path)
    stocks.update({name: symbol})
    save_stocks(stocks, file_path)


def delete_stock(symbol: str, file_path: str):
    """
    Remove the stock with the specified symbol.

    :param symbol: Symbol representing a stock
    :param file_path: Path of the data file
    """

    stocks = load_stocks(file_path)
    if symbol in stocks:
        del stocks[symbol]
        save_stocks(stocks, file_path)


def get_all_stocks(file_path: str, sort_by: str = "name") -> list:
    """
    Get all data for the stocks in the specified file

    :param file_path: Path of storage file
    :param sort_by: Sort the stocks by specific attribute
    :return: List of stocks
    """
    # Get symbols from file
    symbols = load_stocks(file_path)
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

    # Sort by name
    stocks.sort(key=attrgetter(sort_by))
    return stocks
