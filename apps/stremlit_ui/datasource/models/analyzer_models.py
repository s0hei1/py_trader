from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime

from backtrader.analyzers import TradeAnalyzer, DrawDown, PositionsValue, TimeReturn


@dataclass(frozen=True)
class TradeAnalyzerModel:
    total_total: int
    total_open: int
    total_closed: int

    streak_won_current: int
    streak_won_longest: int
    streak_lost_current: int
    streak_lost_longest: int

    pnl_gross_total: float
    pnl_gross_average: float
    pnl_net_total: float
    pnl_net_average: float

    won_total: int
    won_pnl_total: float
    won_pnl_average: float
    won_pnl_max: float

    lost_total: int
    lost_pnl_total: float
    lost_pnl_average: float
    lost_pnl_max: float

    long_total: int
    long_won: int
    long_lost: int
    long_pnl_total: float
    long_pnl_average: float
    long_pnl_won_total: float
    long_pnl_won_average: float
    long_pnl_won_max: float
    long_pnl_lost_total: float
    long_pnl_lost_average: float
    long_pnl_lost_max: float

    short_total: int
    short_won: int
    short_lost: int
    short_pnl_total: float
    short_pnl_average: float
    short_pnl_won_total: float
    short_pnl_won_average: float
    short_pnl_won_max: float
    short_pnl_lost_total: float
    short_pnl_lost_average: float
    short_pnl_lost_max: float

    len_total: int
    len_average: float
    len_max: int
    len_min: int
    len_won_total: int
    len_won_average: float
    len_won_max: int
    len_won_min: int
    len_lost_total: int
    len_lost_average: float
    len_lost_max: int
    len_lost_min: int

    len_long_total: int
    len_long_average: float
    len_long_max: int
    len_long_min: int
    len_long_won_total: int
    len_long_won_average: float
    len_long_won_max: int
    len_long_won_min: int
    len_long_lost_total: int
    len_long_lost_average: float
    len_long_lost_max: int
    len_long_lost_min: int

    len_short_total: int
    len_short_average: float
    len_short_max: int
    len_short_min: int
    len_short_won_total: int
    len_short_won_average: float
    len_short_won_max: int
    len_short_won_min: int
    len_short_lost_total: int
    len_short_lost_average: float
    len_short_lost_max: int
    len_short_lost_min: int

    @classmethod
    def from_trade_analyzer(cls, trade_analyzer: TradeAnalyzer):
        result = {}
        for annotation in cls.__annotations__:
            keys = annotation.split('_')
            analysis = trade_analyzer.get_analysis()
            for k in keys:
                if isinstance(analysis.get(k), dict):
                    analysis = analysis.get(k)
                else:
                    result[annotation] = analysis.get(k)

        return TradeAnalyzerModel(**result)

@dataclass(frozen=True)
class DrawDownAnalyzerModel():
    len_ : int
    drawdown : float
    moneydown : float
    max_len : int
    max_drawdown : float
    max_moneydown : float

    @classmethod
    def from_drawdown_analyzer(cls ,drawdown_analyzer : DrawDown):
        return DrawDownAnalyzerModel(
            len_ = drawdown_analyzer.get_analysis().get('len'),
            drawdown = drawdown_analyzer.get_analysis().get('drawdown'),
            moneydown = drawdown_analyzer.get_analysis().get('moneydown'),
            max_len = drawdown_analyzer.get_analysis().get('max').get('len'),
            max_drawdown = drawdown_analyzer.get_analysis().get('max').get('drawdown'),
            max_moneydown = drawdown_analyzer.get_analysis().get('max').get('moneydown')
        )

@dataclass(frozen=True)
class AnalyzerDataModel:
    name : str
    analyzer : type
    attr_name : str
    kwargs : dict | None = field(default_factory=dict)

@dataclass(frozen=True)
class TimeReturnAnalyzerModel():
    month : datetime
    value : float

    @property
    def is_positive(self) -> bool:
        return self.value > 0

    @property
    def is_negative(self) -> bool:
        return self.value < 0

    def __str__(self):
        return f'Year-month: {self.month.year}-{self.value} Value: {self.value}'

    @classmethod
    def from_time_return_analyzer(cls, time_return_analyzer : TimeReturn) -> list[TimeReturnAnalyzerModel]:
        analysis = time_return_analyzer.get_analysis()
        result = []
        for i in analysis:
            result.append(TimeReturnAnalyzerModel(month = i,value = round(analysis.get(i) * 100, 4)))\

        return result
