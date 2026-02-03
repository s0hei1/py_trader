from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.py_trader.data.models.models import Symbol

class SymbolRepo:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_one(self, symbol: Symbol) -> Symbol:
        self.session.add(symbol)

        await self.session.commit()
        await self.session.refresh(symbol)

        return symbol

    async def read_many(self) -> Sequence[Symbol]:
        result = await self.session.execute(select(Symbol))
        return result.scalars().all()

