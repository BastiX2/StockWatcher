import datetime
import os
import time


def show(stocks: list, refresh: float = 5):
    """
    Print the stocks to display

    :param stocks: List of stocks to be displayed:
    :param refresh: Seconds between display refresh
    """
    try:
        while True:
            # Print current time, a Header with information and the stocks
            print(datetime.datetime.now())
            print('{:>32} {:>10} {:>10} {:>10} {:>10}'.format("Name", "Last Close", "Current", "Change", "Change %"))
            print(*stocks, sep="\n")
            time.sleep(refresh)
            os.system('cls' if os.name == 'nt' else 'clear')
    except KeyboardInterrupt:
        pass
