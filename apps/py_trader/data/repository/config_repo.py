from sqlalchemy import select, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from toolz import last
from apps.py_trader.data.models.models import Config


class ConfigRepo:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def create_config(self, config : Config) -> Config | None:

        self.session.add(config)
        await self.session.commit()
        await self.session.refresh(config)
        return config

    async def read_last_config(self) -> Config | None:
        q = select(Config).order_by(Config.creation_datetime.desc()).limit(1)
        config = (await self.session.execute(q)).scalars().first()

        return config


    async def read_configs_history(self) -> ScalarResult[Config]:
        q = select(Config).order_by(Config.creation_datetime.desc())
        configs = (await self.session.execute(q)).scalars()

        return configs

