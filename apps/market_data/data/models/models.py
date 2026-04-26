from __future__ import annotations
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Flags(Base):
    __tablename__ = 'flags'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    is_first_run: Mapped[bool] = mapped_column(default=False)
    is_development: Mapped[bool]

class Symbol(Base):
    __tablename__ = 'symbols'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(16))

class TimeFrame(Base):
    __tablename__ = 'timeframes'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(16))
    resolution: Mapped[int]

class Broker(Base):
    __tablename__ = 'brokers'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))


class Candle(Base):
    __tablename__ = 'candles'
    id: Mapped[int] = mapped_column(primary_key=True)
    symbol_id : Mapped[int] = mapped_column(ForeignKey('symbols.id'),index = True)
    time_frame_id : Mapped[int] = mapped_column(ForeignKey('timeframes.id'), index = True)
    broker_id : Mapped[int] = mapped_column(ForeignKey('brokers.id'), index = True)
    date_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    open_ : Mapped[float]
    high : Mapped[float]
    low : Mapped[float]
    close : Mapped[float]
    volume : Mapped[float]

    symbol : Mapped[Symbol] = relationship()
    time_frame : Mapped[Symbol] = relationship()
    broker : Mapped[Broker] = relationship()