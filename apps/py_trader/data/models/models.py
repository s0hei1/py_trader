from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from apps.py_trader.data.enums.platform_type import PlatformType
from src.ui.viewmodel.trading_history_vm import TradingHistoryVM


class Base(DeclarativeBase):
    pass


class Flags(Base):
    __tablename__ = 'flags'

    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    maximum_risk_percentage : Mapped[float] = mapped_column(default=1.0)
    default_risk_percentage : Mapped[float] = mapped_column(default=1.0)
    total_balance : Mapped[float] = mapped_column(default=0.0)


class TradingPlatforms(Base):
    __tablename__ = 'trading_platforms'

    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    platform_name : Mapped[str]
    platform_url : Mapped[str]
    platform_type : Mapped[PlatformType]

class Strategies(Base):
    __tablename__ = 'strategies'

    id : Mapped[int] = mapped_column(primary_key=True)
    strategy_name : Mapped[str]
    strategy_type : Mapped[PlatformType]

class PlaceOrderRequest(Base):
    __tablename__ = 'place_order_request'

    id : Mapped[int] = mapped_column(primary_key=True)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True))
    order_type : Mapped[str]
    entry_price : float
    stop_price : float
    tp_price : float
    request_status : Mapped[str]
    external_id : Mapped[int] = mapped_column(primary_key=True)


