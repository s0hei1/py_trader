from typing import Sequence
from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession
from apps.market_data.data.models.models import Broker

class BrokerRepo:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_one(self, broker: Broker) -> Broker:

        q = select(
            exists().where(Broker.name == broker.name)
        )

        is_broker_duplicate = (await self.session.execute(q)).scalar()

        if is_broker_duplicate:
            raise ValueError(f"A broker with {broker.name} name already exists")

        self.session.add(broker)

        await self.session.commit()
        await self.session.refresh(broker)

        return broker

    async def read_many(self) -> Sequence[Broker]:
        result = await self.session.execute(select(Broker))
        return result.scalars().all()