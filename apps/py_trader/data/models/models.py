from __future__ import annotations
from typing import List
from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime,UTC
from apps.py_trader.data.enums.platform_type import PlatformType
from apps.py_trader.data.enums.strategy_type import StrategyType
from apps.py_trader.data.enums.times_frame_enum import TimeFrameEnum


class Base(DeclarativeBase):
    pass


class Flags(Base):
    __tablename__ = 'flags'

    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    is_first_run : Mapped[bool] = mapped_column(default=False)
    is_development : Mapped[bool]


class Config(Base):
    __tablename__ = 'configs'
    id : Mapped[int] = mapped_column(primary_key=True)
    creation_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    maximum_risk_percentage : Mapped[float] = mapped_column(default=1.0)
    default_risk_percentage : Mapped[float] = mapped_column(default=1.0)
    total_balance : Mapped[float] = mapped_column(default=0.0)

class Strategy(Base):
    __tablename__ = 'strategies'

    id : Mapped[int] = mapped_column(primary_key=True)
    strategy_name : Mapped[str]
    strategy_type : Mapped[StrategyType]


#
# class TradingPlatform(Base):
#     __tablename__ = 'trading_platforms'
#
#     id : Mapped[int] = mapped_column(primary_key=True)
#     platform_name : Mapped[str]
#     platform_url : Mapped[str]
#     platform_type : Mapped[PlatformType]
#
# class TradingAccounts(Base):
#     __tablename__ = 'trading_accounts'
#
#     id : Mapped[int] = mapped_column(primary_key=True)
#     username : Mapped[str]
#     password : Mapped[str]
#     # trading_platform_id : Mapped[TradingPlatform]
#     #
#     # trading_platform : Mapped[TradingPlatform] = relationship('TradingPlatform')
#
#

class Symbol(Base):
    __tablename__ = 'symbols'
    id : Mapped[int] = mapped_column(primary_key=True)
    base_currency : Mapped[str]
    quote_currency : Mapped[str]

class PatternGroup(Base):
    __tablename__ = 'pattern_groups'
    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str]
    is_active : Mapped[bool] = mapped_column(default=True)

    patterns: Mapped[List[Pattern]] = relationship(back_populates="pattern_group")

class Pattern(Base):
    __tablename__ = 'patterns'
    id : Mapped[int] = mapped_column(primary_key=True)
    pattern_group_id : Mapped[int] = mapped_column(ForeignKey('pattern_groups.id'))
    pattern_first_candle : Mapped[datetime] = mapped_column(DateTime(timezone=True))
    pattern_last_candle : Mapped[datetime] = mapped_column(DateTime(timezone=True))
    is_active : Mapped[bool] = mapped_column(default=True)
    time_frame : Mapped[TimeFrameEnum]
    symbol_id : Mapped[int] = mapped_column(ForeignKey('symbols.id'))

    symbol : Mapped[Symbols] = relationship()
    pattern_group: Mapped[PatternGroup] = relationship(back_populates="patterns")

#
#
# #DocTable Trading Scope
# class PlaceOrderRequest(Base):
#     __tablename__ = 'place_order_request'
#
#     id : Mapped[int] = mapped_column(primary_key=True)
#     created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True))
#     order_type : Mapped[str]
#     entry_price : float
#     stop_price : float
#     tp_price : float
#     request_status : Mapped[str]
#     external_id : Mapped[int] = mapped_column(primary_key=True)
#
#
