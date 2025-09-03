from dataclasses import dataclass
from typing import Sequence
import csv
from datetime import datetime
import pandas as pd
from third_party.candlestic.candle import Candle
import pandas as pd

@dataclass
class Chart:
    candles : Sequence[Candle]
    time_frame : str | None = None
    _indicators : dict | None = None

    def __init__(self, candles : Sequence[Candle], time_frame : str | None = None):
        self.candles = candles
        self.time_frame = time_frame

    def __getitem__(self, item):
        return self.candles[item]

    def __iter__(self):
        return iter(self.candles)

    def add_indicator(self, indicator_name ,indicator):
        self._indicators[indicator_name] = indicator

    def to_dataframe(self):

        data = [(i.datetime, i.open, i.high,i.low, i.close, self.time_frame) for i in self]

        df = pd.DataFrame(
            data= data,
            columns=['datetime', 'open','high','low','close', 'time_frame']
        )

        return df


    @classmethod
    def from_pd_dataframe(cls, data_frame : pd.DataFrame, time_frame : str) -> 'Chart':
        candles = []

        for i, row in data_frame.iterrows():
            candle = Candle(
                open= row['Open'],
                high= row['High'],
                low= row['Low'],
                close= row['Close'],
            )
            candles.append(candle)

        return cls(candles)

    @classmethod
    def from_csv(cls, file_path: str) -> 'Chart':
        candles = []
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header row
            for row in reader:
                open_, high, low, close, dt_str = row

                candle = Candle(
                    open=float(open_),
                    high=float(high),
                    low=float(low),
                    close=float(close),
                    datetime=datetime.fromisoformat(dt_str)
                )
                candles.append(candle)
        return cls(candles)
