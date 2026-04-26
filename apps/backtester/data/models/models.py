from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship
from sqlalchemy.testing.schema import mapped_column
from apps.backtester.data.enums import TriggerType, StoplossType

class BaseModel(DeclarativeBase):
    pass

class Setup(BaseModel):

    id : Mapped[int] = mapped_column(primary_key=True)
    description : Mapped[str] = mapped_column(String(64))
    trigger_type : Mapped[TriggerType]
    line_a_name : Mapped[str] = mapped_column(String(32))
    line_a_id : Mapped[str] = mapped_column(String(32))
    line_b_name : Mapped[str] = mapped_column(String(32))
    line_b_id : Mapped[str] = mapped_column(String(32))

class RiskManagement(BaseModel):
    id : Mapped[int] = mapped_column(primary_key=True)
    description : Mapped[str] = mapped_column(String(64))
    stop_loss_type : Mapped[StoplossType]
    stop_loss_size : Mapped[float]
    take_profit_size : Mapped[float]

class Strategy(BaseModel):
    id : Mapped[int] = mapped_column(primary_key=True)
    description : Mapped[str] = mapped_column(String(64))
    setup_id : Mapped[int] = mapped_column(ForeignKey('setup.id'))
    risk_management_id : Mapped[int] = mapped_column(ForeignKey('risk_management.id'))

    setup : Mapped[Setup] = relationship(back_populates="strategy")
    risk_management : Mapped[Setup] = relationship(back_populates="strategy")

# class BacktestStatement(BaseModel):
#     pass
#
# class BackTestStatementDetails(BaseModel):
#     pass
