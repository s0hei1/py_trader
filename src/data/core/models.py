from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

class Base(DeclarativeBase):
    pass


class Flags(Base):
    __tablename__ = 'flags'
    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    risk_percentage : Mapped[float] = mapped_column(default=0.0)
    total_balance : Mapped[float] = mapped_column(default=0.0)


class Pattern(Base):
    __tablename__ = 'pattern'

    id : Mapped[int] = mapped_column(primary_key=True)
    pattern_start_date_time : Mapped[datetime] = mapped_column(DateTime(timezone=True))
    pattern_end_date_time : Mapped[datetime] = mapped_column(DateTime(timezone=True))
    pattern_time_frame : Mapped[str]
    symbol_name : Mapped[str]

