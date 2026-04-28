from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backtester.data.models.models import StatementDocument


class StatementDocumentRepo:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_one(self, statement: StatementDocument) -> StatementDocument:
        self.session.add(statement)
        await self.session.commit()
        await self.session.refresh(statement)
        return statement

    async def read_many(self) -> Sequence[StatementDocument]:
        q = select(StatementDocument)
        result = await self.session.execute(q)

        return result.scalars().all()
