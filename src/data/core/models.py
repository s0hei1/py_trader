from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

class Base(DeclarativeBase):
    pass


class Flags(Base):
    __tablename__ = 'flags'
    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    risk_percentage : Mapped[float] = mapped_column(default=0.0)
    total_balance : Mapped[float] = mapped_column(default=0.0)


# class PatternType(Base):
#     __tablename__ = 'pattern_type'
#     id : Mapped[int] = mapped_column(primary_key=True)
#     name : Mapped[str] = mapped_column(String(32))

class Pattern(Base):
    __tablename__ = 'pattern'

    id : Mapped[int] = mapped_column(primary_key=True)
    pattern_start_date_time : Mapped[datetime] = mapped_column(DateTime(timezone=True))
    pattern_end_date_time : Mapped[datetime] = mapped_column(DateTime(timezone=True))
    pattern_time_frame : Mapped[str]
    symbol_name : Mapped[str]

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

    @classmethod
    def get_columns_name(cls, exclude : list[str]):
        result =  [col.name for col in cls.__table__.columns]

        for ex in exclude:
            result.remove(ex)

        return result

class PlaceOrder(Base):
    __tablename__ = 'pattern_trading'

    id : Mapped[int] = mapped_column(primary_key=True)
    order_code : Mapped[str] = mapped_column(unique=True)
    order_ticket : Mapped[int]
    pattern_id : Mapped[int] = mapped_column(ForeignKey('pattern.id'))