import asyncio

from src.tools.di.container import Container
from third_party.auto_trader.auto_trader import SimpleAutoTrader
from third_party.auto_trader.risk_managers.static_risk_manager import StaticRiskManager
from third_party.auto_trader.strategies.simple_ma_strategy import SimpleMACrossStrategy
from third_party.candlestic.defaults import ClassicFractalTimeFrames, DefaultSymbols


class AutoTradingVM(object):

    def __init__(self):
        self.flags = Container.flags_repo()

    def run_simple_ma_strategy(self):
        flags = self.flags.get_or_config_flags()

        auto_trader = SimpleAutoTrader(
            strategy=SimpleMACrossStrategy(),
            symbol=DefaultSymbols.gbp_usd,
            timeframe=ClassicFractalTimeFrames.H1,
            risk_manager=StaticRiskManager(
                balance=flags.total_balance,
                risk_size=flags.risk_percentage
            )
        )

        asyncio.run(auto_trader.run())


