from __future__ import annotations
from datetime import datetime, UTC
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime,func


class Base(DeclarativeBase):
    pass

class Experience(Base):
    __tablename__ = 'experiences'

    id : Mapped[int] = mapped_column(primary_key=True)
    note : Mapped[str] = mapped_column(default='')
    created_at : Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )