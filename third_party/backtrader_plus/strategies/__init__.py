from .kama_buy_strategy import KamaBuyStrategy,KamaSellStrategy
from .kama_buy_v2_strategy import KamaBuyV2Strategy
from .moving_average_cross_strategy import MovingAverageCrossStrategy
from .moving_average_cross_v2_strategy import MovingAverageCrossV2Strategy
from .trex_moving_buy_strategy import TrexMovingBuyStrategy


__all__ = [
    'KamaBuyStrategy'
]

strategies_dict = {
    'Kama Buy Strategy' : KamaBuyStrategy,
    'Trex Moving Buy Strategy' : TrexMovingBuyStrategy,
    'Moving Average Cross Strategy' : MovingAverageCrossStrategy,
    'Kama Buy V2 Strategy' : KamaBuyV2Strategy,
    'Moving Average Cross V2 Strategy' : MovingAverageCrossV2Strategy,
}