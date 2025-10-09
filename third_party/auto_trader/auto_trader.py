from typing import Any
import datetime as dt
from third_party import mt5_overhead as mt5
from third_party.auto_trader.models import TradeSignal
from third_party.auto_trader.protocols import StrategyProtocol, RiskManagerProtocol
from third_party.candlestic import Symbol, TimeFrame

class SimpleAutoTrader:

    def __init__(self,strategy: StrategyProtocol,risk_manager : RiskManagerProtocol, symbol : Symbol, timeframe : TimeFrame, ):
        self.symbol = symbol
        self.strategy = strategy
        self.timeframe = timeframe
        self.risk_manager = risk_manager

    async def run(self, history_initial_dt: dt.datetime | None = None, ):

        if history_initial_dt is None:
            history_initial_dt = dt.datetime.now(dt.UTC) - dt.timedelta(minutes=self.timeframe.included_m1 * 100)

        live_chart_stream = mt5.stream_chart_data(
            self.symbol,
            self.timeframe,
            as_chart=True
        )

        print("StrategyA Started to running")

        async for chart in live_chart_stream:

            if not self.strategy.is_initialized:
                self.strategy.initialize(chart)
                continue

            print("StrategyA is running")

            trade_signal : TradeSignal | None= self.strategy.next(chart)

            print("signal is: ", trade_signal)

            if trade_signal is None:
                continue

            set_order_result = mt5.set_pending_order(
                order_type = trade_signal.order_type,
                symbol = self.symbol,
                volume = round(self.risk_manager.calculate_size(trade_signal.entry_price, trade_signal.stop_loss_price)[1] / 100000, 2),
                entry_price = trade_signal.entry_price,
                stop_loss = trade_signal.stop_loss_price,
                take_profit = trade_signal.take_profit_price,
                external_id = trade_signal.external_trade_id,
            )

            print(set_order_result.message)

            if set_order_result.has_error:
                self._notify_error(set_order_result.message)
            else:
                self._notify_order()

    def _notify_order(self):
        pass

    def _notify_error(self, error_message : str):
        pass

