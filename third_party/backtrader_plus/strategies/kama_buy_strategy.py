import backtrader as bt
from backtrader.indicators import CrossOver, AverageTrueRange, AdaptiveMovingAverage, MovingAverageSimple
from sqlalchemy import result_tuple


class KamaBuyStrategy(bt.Strategy):

    @staticmethod
    def get_params(as_tuple: bool = False) -> dict | tuple:
        p_ = {
            'kama_period': 24,
            'atr_period': 24,
            'tp_size': 7,
            'stop_size': 2,
            'risk': 1.5,
            'balance': 10000,
        }
        if as_tuple:
            result_ = [(i, p_[i]) for i in p_]
            return tuple(result_)

        return p_

    params = get_params(as_tuple=True)

    def __init__(self):
        self.ma = AdaptiveMovingAverage(period=self.p.kama_period)
        self.cross_over = CrossOver(self.data.close, self.ma)
        self.atr = AverageTrueRange(period=self.p.atr_period)
        self.sma240 = MovingAverageSimple(period=240)
        self.trade_id = 1

    def generate_trade_id(self):
        self.trade_id += 1
        return self.trade_id

    def next(self):
        if self.cross_over[0] > 0 and self.sma240[0] < self.data.close[0]:
            entry = self.data.close[0]
            atr = self.atr[0]
            tp = entry + (atr * self.p.tp_size)

            tp = round(tp, 5)

            stop = entry - (atr * self.p.stop_size)
            stop = round(stop, 5)

            trade_size = self._get_size(entry, stop, self.p.balance, self.p.risk)

            self.buy_bracket(
                exectype=bt.Order.Market,
                stopprice=stop,
                limitprice=tp,
                size=trade_size,
                tradeid=self.generate_trade_id(),
            )

    def _get_size(
            self,
            entry_price: float,
            stop_price: float,
            balance: int = 10000,
            risk: float = 1,
    ):
        risk_amount = balance * (risk / 100)
        stop_size = abs(entry_price - stop_price)
        units = risk_amount / stop_size
        return int(units)
