from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache
from typing import Sequence, Any, Callable, TypeAlias
import csv
from datetime import datetime, UTC
from numpy._typing import NDArray

from third_party.candlestic.candle import Candle
import pandas as pd
import numpy as np
from third_party.candlestic.indicator import Indicator
from more_itertools import last

OnChartUpdate: TypeAlias = Callable[[Sequence[Candle]], Any]


@dataclass
class Chart:
    candles: Sequence[Candle]
    indicators_name: list[str]
    timeframe: str | None = None
    on_chart_update: OnChartUpdate | None = None

    def __init__(self,
                 candles: Sequence[Candle],
                 timeframe: str | None = None,
                 on_chart_update: OnChartUpdate | None = None):
        self.candles = candles
        self.timeframe = timeframe
        self.indicators_name = []
        self.on_chart_update = on_chart_update

    def add_indicator(self, indicator: Indicator):

        if len(indicator) != len(self.candles):
            raise Exception("Length of indicator values must equal with Candles length")

        if hasattr(self, indicator.name):
            raise Exception(f"an indicator with name {indicator.name} is exists")

        setattr(self, indicator.name, indicator.values)

    def to_dataframe(self):

        data = [(i.date_time, i.open, i.high, i.low, i.close, self.timeframe) for i in self.candles]

        df = pd.DataFrame(
            data=data,
            columns=['datetime', 'open', 'high', 'low', 'close', 'timeframe']
        )

        return df

    def separate_ochl(self, to_ndarray: bool = False) -> tuple[
                                                             np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray] | \
                                                         Sequence[tuple[float, float, float, float, float]]:
        data = [(i.open, i.close, i.high, i.low, i.date_time.timestamp()) for i in self.candles]

        if to_ndarray:
            arr = np.array(data, dtype=float)
            opens, closes, highs, lows, times = arr.T
            return (opens, closes, highs, lows, times)

        return data

    def update_chart(self, new_candles: Sequence[Candle]) -> None:

        if new_candles is None or new_candles == []:
            return None

        candles = list(self.candles)

        last_candle = last(candles)
        new_candles_for_add = [i for i in new_candles if i.date_time > last_candle.date_time]

        for candle in new_candles_for_add:
            candles.append(candle)

        self.candles = candles

        if self.on_chart_update is not None:
            self.on_chart_update(self.candles)

    @classmethod
    def from_pd_dataframe(cls, data_frame: pd.DataFrame, time_frame: str) -> 'Chart':
        candles = []

        for i, row in data_frame.iterrows():
            candle = Candle(
                open=row['Open'],
                high=row['High'],
                low=row['Low'],
                close=row['Close'],
            )
            candles.append(candle)

        return cls(candles)

    @classmethod
    def from_csv(cls, file_path: str) -> Chart:
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
                    date_time=datetime.fromisoformat(dt_str)
                )
                candles.append(candle)
        return cls(candles)

    @classmethod
    def from_mt5_data(cls, data: NDArray[tuple], timeframe: TimeFrame) -> Chart:
        return Chart(
            candles=[Candle(
                date_time=datetime.fromtimestamp(i[0], UTC),
                open=i[1],
                high=i[2],
                low=i[3],
                close=i[4]
            ) for i in data],
            timeframe=timeframe.name,
        )

    def __setattr__(self, key, value):
        if not hasattr(self, "indicators_name"):
            super().__setattr__("indicators_name", [])

        if isinstance(value, Indicator):
            self.indicators_name.append(key)

        super().__setattr__(key, value)

    def __delattr__(self, key):
        if hasattr(self, key) and isinstance(getattr(self, key), Indicator):
            if key in self.indicators_name:
                self.indicators_name.remove(key)

        super().__delattr__(key)

    def __getitem__(self, col_name: str):

        if col_name in Candle.get_annotations():
            data = [getattr(i, col_name) for i in self.candles]
            return np.array(data, dtype=float)

        if hasattr(self, col_name) and isinstance(getattr(self, col_name), Indicator):
            indicator: Indicator = getattr(self, col_name)
            return indicator.values

        raise Exception("your provided col name is not exists")

    def __iter__(self):
        return iter(self.candles)

    def __len__(self):
        return len(self.candles)

    def __add__(self, other : Chart) -> Chart:
        self.update_chart(other.candles)
        return self

