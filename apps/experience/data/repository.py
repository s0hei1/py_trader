from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Sequence
from apps.experience.data.models import Experience


class ExperienceRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_one(self, experience: Experience) -> Experience:
        self.session.add(experience)
        await self.session.commit()
        await self.session.refresh(experience)
        return experience

    async def update(self, experience: Experience) -> Experience:
        await self.session.merge(experience)
        await self.session.commit()
        await self.session.refresh(experience)
        return experience

    async def read_one(self, id: int) -> Experience | None:
        result = await self.session.execute(
            select(Experience).where(Experience.id == id)
        )
        return result.scalar_one_or_none()

    async def read_many(self) -> Sequence[Experience]:
        result = await self.session.execute(select(Experience))
        return result.scalars().all()
