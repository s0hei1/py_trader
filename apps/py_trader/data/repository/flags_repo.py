from sqlalchemy import select
from sqlalchemy.orm import Session
from apps.py_trader.data.models.models import Flags

class FlagsRepo:
    _flags_id: int = 1

    def __init__(self, session: Session):
        self.session = session

    def get_or_config_flags(self) -> Flags:
        q = select(Flags).where(Flags.id == self._flags_id)

        flags = self.session.execute(q).scalar_one_or_none()

        if flags is not None:
            return flags

        flags = Flags(
            id=self._flags_id,
            is_development = True
        )

        self.session.add(flags)
        self.session.commit()
        self.session.refresh(flags)

        return flags

    def set_flags(self,is_development : bool =None) -> Flags:

        flags = self.get_or_config_flags()

        if is_development is not None:
            flags.is_development = is_development

        self.session.commit()
        self.session.refresh(flags)
        return flags
