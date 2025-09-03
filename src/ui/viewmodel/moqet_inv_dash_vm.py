import pandas as pd


class TradeVM():

    _risk_percentage = 1
    volume_size = 1000

    @property
    def get_risk_percentage(self):
        return self._risk_percentage

    def set_risk_percentage(self, new_value : str | int):
        self._risk_percentage = int(new_value)
