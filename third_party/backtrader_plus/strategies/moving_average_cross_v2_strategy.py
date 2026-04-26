from backtrader import Strategy, Order, Trade
from backtrader.indicators import DicksonMovingAverage, WeightedMovingAverage, AdaptiveMovingAverage, \
    CrossOver

from third_party.backtrader_plus.indicators.atr_tpsl import ATR_TPSL


class MovingAverageCrossV2Strategy(Strategy):

    @staticmethod
    def get_params(as_tuple: bool = False) -> dict | tuple:
        p_ = {
            'fast_ma_period': 8,
            'slow_ma_period': 24,
            'structure_ma_period': 120,
            'atr_period': 24,
            'risk_size': 1,
            'max_parallel_trades': 5,
            'tp_size': 8,
            'sl_size': 1.8,
        }
        if as_tuple:
            result_ = [(i, p_[i]) for i in p_]
            return tuple(result_)

        return p_

    params = get_params(as_tuple=True)

    def __init__(self):
        self.structure_ma = WeightedMovingAverage(period=self.p.structure_ma_period)

        self.fast_ma = DicksonMovingAverage(period=self.p.fast_ma_period)
        self.slow_ma = AdaptiveMovingAverage(period=self.p.slow_ma_period)

        atr_tpsl = ATR_TPSL(atr_period=self.p.atr_period, tp_size=self.p.tp_size, sl_size=self.p.sl_size)
        self.tp = atr_tpsl.tp
        self.sl = atr_tpsl.sl

        self.cross_over = CrossOver(self.fast_ma, self.slow_ma)

        self.open_trades_counter = 0
        self.trade_id = 1

    def generate_trade_id(self):
        self.trade_id += 1
        return self.trade_id

    def next(self):
        if self.structure_ma[0] > self.data.close[0] and self.cross_over[
            0] > 0 and self.open_trades_counter <= self.p.max_parallel_trades:
            trade_size = self._get_size(self.data.close[0], self.sl[0])

            self.buy_bracket(
                exectype=Order.Market,
                stopprice=self.sl[0],
                limitprice=self.tp[0],
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

    def notify_trade(self, trade: Trade):
        if trade.justopened:
            self.open_trades_counter += 1
        if trade.isclosed:
            self.open_trades_counter -= 1


"""brute force_ top results"""
# {'settings': {'tp_size': 8, 'sl_size': 1.8, 'max_parallel_trades': 4}, 'value': 1010841.4437694765}
# {'settings': {'tp_size': 8, 'sl_size': 1.6, 'max_parallel_trades': 4}, 'value': 1010307.6304103379}
# {'settings': {'tp_size': 8, 'sl_size': 1.8, 'max_parallel_trades': 1}, 'value': 1008471.9579474302}
# {'settings': {'tp_size': 8, 'sl_size': 1.6, 'max_parallel_trades': 1}, 'value': 1007449.9965154479}