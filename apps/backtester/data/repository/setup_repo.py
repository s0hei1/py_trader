from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backtester.data.models.models import Setup


class SetupRepo:

    def __init__(self, session : AsyncSession):
        self.session = session

    async def create_one(self, setup : Setup) -> Setup:
        self.session.add(setup)
        await self.session.commit()
        await self.session.refresh(setup)
        return setup

    async def read_many(self) -> Sequence[Setup]:
        q = select(Setup)
        result = await self.session.execute(q)

        return result.scalars().all()
