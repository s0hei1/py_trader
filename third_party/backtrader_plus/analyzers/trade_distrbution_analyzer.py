import backtrader as bt
from collections import defaultdict

class TradeDistributionAnalyzer(bt.Analyzer):

    def start(self):
        self.bar_trades = defaultdict(int)

    def notify_trade(self, trade):
        if trade.isclosed:
            bar = len(self.strategy)
            self.bar_trades[bar] += 1

    def get_analysis(self):
        total_trades = sum(self.bar_trades.values())
        unique_bars = len(self.bar_trades)

        density = total_trades / unique_bars if unique_bars > 0 else 0

        return {
            "total_trades": total_trades,
            "bars_with_trades": unique_bars,
            "trade_density": density,
            "distribution": dict(self.bar_trades)
        }