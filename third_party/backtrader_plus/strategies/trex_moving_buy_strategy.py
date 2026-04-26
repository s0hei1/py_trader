from backtrader.indicators import MovingAverageSimple, HullMovingAverage,CrossOver
from backtrader import Strategy,Order,Trade

from third_party.backtrader_plus.indicators.atr_tpsl import ATR_TPSL


class TrexMovingBuyStrategy(Strategy):

    @staticmethod
    def get_params(as_tuple: bool = False) -> dict | tuple:
        p_ = {
            'hma_period': 24,
            'atr_period': 24,
            'structure_sma_period': 120,
            'risk': 1.5,
            'max_parallel_trades': 3,
            'tp_size': 9,
            'sl_size': 1.2,
        }
        if as_tuple:
            result_ = [(i, p_[i]) for i in p_]
            return tuple(result_)

        return p_

    params = get_params(as_tuple=True)

    def __init__(self):
        self.sma_structure = MovingAverageSimple(period=self.p.structure_sma_period)
        self.hma = HullMovingAverage(period=24)
        atr_tpsl = ATR_TPSL(atr_period=24, tp_size=self.p.tp_size, sl_size=self.p.sl_size)
        self.tp = atr_tpsl.tp
        self.sl = atr_tpsl.sl
        self.cross_over = CrossOver(self.data.close, self.hma)
        self.signal_counter = 0
        self.open_trades_counter = 0
        self.trade_id = 1

    def generate_trade_id(self):
        self.trade_id += 1
        return self.trade_id

    def next(self):
        if self.sma_structure[0] > self.data.close[0] and self.cross_over[
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
            balance: int = 1000,
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
#  {'settings': {'tp_size': 9, 'sl_size': 1.2, 'max_parallel_trades': 5},'value': 1002458.6843351158}
#  {'settings': {'tp_size': 9, 'sl_size': 1.2, 'max_parallel_trades': 3},'value': 1001983.0166926656}
#  {'settings': {'tp_size': 8, 'sl_size': 1.2, 'max_parallel_trades': 5},'value': 1001975.0422592587}
#  {'settings': {'tp_size': 8, 'sl_size': 1.2, 'max_parallel_trades': 3},'value': 1001665.4269156335}
