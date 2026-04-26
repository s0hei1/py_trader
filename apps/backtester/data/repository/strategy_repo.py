from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backtester.data.models.models import Strategy


class StrategyRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_one(self, Strategy: Strategy) -> Strategy:
        self.session.add(Strategy)
        await self.session.commit()
        await self.session.refresh(Strategy)
        return Strategy

    async def read_many(self) -> Sequence[Strategy]:
        q = select(Strategy)
        result = await self.session.execute(q)

        return result.scalars().all()
