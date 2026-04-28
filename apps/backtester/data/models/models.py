from __future__ import annotations
from sqlalchemy import String, ForeignKey,JSON,DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship
from sqlalchemy.testing.schema import mapped_column
from apps.backtester.data.enums.enums import TriggerType, StoplossType



class Base(DeclarativeBase):
    pass

class Setup(Base):
    __tablename__ = 'setups'

    id : Mapped[int] = mapped_column(primary_key=True)
    description : Mapped[str] = mapped_column(String(64))
    trigger_type : Mapped[TriggerType]

    line_a_name : Mapped[str] = mapped_column(String(32))
    line_a_id : Mapped[int]
    line_a_period : Mapped[int | None]
    line_b_name : Mapped[str] = mapped_column(String(32))
    line_b_id : Mapped[int]
    line_b_period : Mapped[int | None]



class RiskManagement(Base):
    __tablename__ = 'risk_managements'

    id : Mapped[int] = mapped_column(primary_key=True)
    description : Mapped[str] = mapped_column(String(64))
    stop_loss_type : Mapped[StoplossType]
    stop_loss_size : Mapped[float]
    take_profit_size : Mapped[float]

class Strategy(Base):
    __tablename__ = 'strategies'

    id : Mapped[int] = mapped_column(primary_key=True)
    description : Mapped[str] = mapped_column(String(64))
    setup_id : Mapped[int] = mapped_column(ForeignKey('setups.id'))
    risk_management_id : Mapped[int] = mapped_column(ForeignKey('risk_managements.id'))

    setup : Mapped[Setup] = relationship(backref="setup_strategies")
    risk_management : Mapped[RiskManagement] = relationship(backref="risk_management_strategies")

class StatementDocument(Base):
    __tablename__ = 'statements'

    id : Mapped[int] = mapped_column(primary_key=True)

    strategy_name : Mapped[str] = mapped_column(String(32))
    strategy_idea : Mapped[str] = mapped_column(String(32))

    fine_options : Mapped[JSON] = mapped_column(String(32))
    annual_return : Mapped[JSON] = mapped_column(String(32))

    symbol_name : Mapped[str] = mapped_column(String(32))
    time_frame : Mapped[str] = mapped_column(String(32))
    data_start_datetime : Mapped[DateTime]
    data_end_datetime : Mapped[DateTime]
    data_length : Mapped[int]
    data_range_ratio : Mapped[float | None]

    balance_value : Mapped[float]
    total_trades : Mapped[int]
    open_trades : Mapped[int]
    close_trades : Mapped[int]

    pnl_total_won : Mapped[float]
    pnl_total_lost : Mapped[float]
    pnl_net : Mapped[float]

    max_win_streak : Mapped[int]
    max_lost_streak : Mapped[int]

    draw_down_max : Mapped[float]
    draw_down_relative : Mapped[float]
    draw_down_avg : Mapped[float]

    len_trades_max : Mapped[int]
    len_trades_avg : Mapped[float]
    len_trades_won_max : Mapped[int]
    len_trades_won_avg : Mapped[float]
    len_trades_lost_max : Mapped[int]
    len_trades_lost_avg : Mapped[float]

