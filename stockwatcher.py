import os
import sys

from api import iexwrapper
from display import console


class DisplayTypes:
    CONSOLE = "console"
    WEB = "web"


if __name__ == '__main__':
    # Validate
    if not len(sys.argv) == 3:
        sys.exit("Provide all arguments")

    # Parse agrv
    display_type = sys.argv[1]
    refresh = float(sys.argv[2])

    # Get file absolute path and retrieve data
    root_path = os.path.dirname(os.path.abspath(__file__))
    file = os.path.join(root_path, "data.txt")
    stocks = iexwrapper.get_all_stocks(file)

    if display_type == DisplayTypes.CONSOLE:
        # Show data on console
        console.show(stocks, refresh)
    elif display_type == DisplayTypes.WEB:
        # Show data on web interface
        sys.exit("Not implemented yet")
    else:
        sys.exit(f"Unknown display type: {display_type}")




