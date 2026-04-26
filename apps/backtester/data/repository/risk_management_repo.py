from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backtester.data.models.models import RiskManagement

class RiskManagementRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_one(self, risk_management: RiskManagement) -> RiskManagement:
        self.session.add(risk_management)
        await self.session.commit()
        await self.session.refresh(risk_management)
        return risk_management

    async def read_many(self) -> Sequence[RiskManagement]:
        q = select(RiskManagement)
        result = await self.session.execute(q)

        return result.scalars().all()
