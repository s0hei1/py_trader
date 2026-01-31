from sqlalchemy import select, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from apps.py_trader.data.exc import NoResultException
from apps.py_trader.data.models.models import Strategy


class StrategyRepo:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, strategy: Strategy):
        self.session.add(strategy)
        await self.session.commit()
        await self.session.refresh(strategy)

        return strategy

    async def read_many(self) -> ScalarResult[Strategy]:
        q = select(Strategy)
        q_result = (await self.session.execute(q)).scalars()

        return q_result

    async def read_one(self, id: int) -> Strategy:
        q = select(Strategy).where(Strategy.id == id)

        q_result = (await self.session.execute(q)).scalar_one_or_none()

        if q_result is None:
            raise NoResultException(f"There is no strategy with id {id}")

        return q_result

    async def update(self,
                              id: int,
                              strategy_name: str,
                              strategy_type: str,
                              ):

        strategy = await self.read_one(id)

        strategy.name = strategy_name
        strategy.type = strategy_type
        await self.session.commit()
        await self.session.refresh(strategy)
        return strategy

