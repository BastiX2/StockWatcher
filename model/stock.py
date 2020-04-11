"""Model for a Stockmarket share"""


class Stock:
    def __init__(self, name: str, symbol: str, value_last_close: float,
                 value_current: float, change: float, change_procent: float):
        self._name = name
        self._symbol = symbol
        self._value_last_close = value_last_close
        self._value_current = value_current
        self._change = change
        self._change_procent = change_procent

    @property
    def name(self):
        return self._name

    @property
    def symbol(self):
        return self._symbol

    @property
    def value_last_close(self):
        return self._value_last_close

    @property
    def value_current(self):
        return self._value_current

    @property
    def change(self):
        return self._change

    @property
    def change_procent(self):
        return self._change_procent

    def __eq__(self, other):
        if isinstance(other, Stock):
            return other._name == other._name
        return False

    def __repr__(self):
        return '{:>32} {:>10} {:>10} {:>10} {:>10}'.format(f"{self._name}({self._symbol})",
                                                           self._value_last_close,
                                                           self._value_current,
                                                           self._change,
                                                           self._change_procent)
