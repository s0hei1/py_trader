from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.py_trader.data.models.models import PatternGroup


class PatternGroupRepo:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_one(self, group: PatternGroup) -> PatternGroup:
        self.session.add(group)

        await self.session.commit()
        await self.session.refresh(group)

        return group

    async def read_many(self) -> Sequence[PatternGroup]:
        result = await self.session.execute(select(PatternGroup))
        return result.scalars().all()