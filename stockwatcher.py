import os

from api import iexwrapper
from display import console


if __name__ == '__main__':
    # Get file absolute path and retrieve data
    root_path = os.path.dirname(os.path.abspath(__file__))
    file = os.path.join(root_path, "data.txt")
    stocks = iexwrapper.get_all_stocks(file)

    # Show data on console
    console.show(stocks, 2)



