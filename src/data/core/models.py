from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Flags(Base):
    __tablename__ = 'flags'
    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    risk_percentage : Mapped[float] = mapped_column(default=0.0)
    total_balance : Mapped[float] = mapped_column(default=0.0)
