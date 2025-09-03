import pandas as pd
from third_party.candlestic import Symbol

class TradeVM():

    _risk_percentage : float = 1
    _volume_size : float= 1000

    @property
    def volume_size(self):
        return self._volume_size

    @property
    def risk_percentage(self):
        return self._risk_percentage


    def set_risk_percentage(self, new_value : str | int):
        self._risk_percentage = float(new_value)

    def set_volume_size(self, new_value : str | int):
        self._volume_size = float(new_value)



