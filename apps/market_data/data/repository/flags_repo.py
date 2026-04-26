from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.py_trader.data.models.models import Flags


class FlagsRepo:
    _flags_id: int = 1

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_config_flags(self) -> Flags:
        q = select(Flags).where(Flags.id == self._flags_id)
        flags = (await self.session.execute(q)).scalar_one_or_none()

        if flags is not None:
            return flags

        flags = Flags(
            id=self._flags_id,
            is_development=True,
            is_first_run=True,
        )

        self.session.add(flags)
        await self.session.commit()
        await self.session.refresh(flags)

        return flags

    async def set_flags(self, is_development: bool | None = None) -> Flags:

        flags = await self.get_or_config_flags()

        if is_development is not None:
            flags.is_development = is_development

        await self.session.commit()
        await self.session.refresh(flags)
        return flags
