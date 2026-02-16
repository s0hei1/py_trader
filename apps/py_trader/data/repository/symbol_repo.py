from typing import Sequence
from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession
from apps.py_trader.data.models.models import Symbol

class SymbolRepo:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_one(self, symbol: Symbol) -> Symbol:

        q = select(
            exists().
            where(Symbol.base_currency == symbol.base_currency, Symbol.quote_currency == symbol.quote_currency)
        )

        is_symbol_duplicate = (await self.session.execute(q)).scalar()

        if is_symbol_duplicate:
            raise ValueError(f"A symbol with {symbol} name already exists")

        self.session.add(symbol)

        await self.session.commit()
        await self.session.refresh(symbol)

        return symbol

    async def read_many(self) -> Sequence[Symbol]:
        result = await self.session.execute(select(Symbol))
        return result.scalars().all()

