from sqlalchemy import select
from sqlalchemy.orm import Session

from src.data.core.models import Flags


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
            id=self._flags_id
        )

        self.session.add(flags)
        self.session.commit()
        self.session.refresh(flags)

        return flags

    def set_flags(self,
                  risk_percentage=None,
                  total_balance=None) -> Flags:

        flags = self.get_or_config_flags()

        if risk_percentage is not None:
            flags.risk_percentage = risk_percentage
        if total_balance is not None:
            flags.total_balance = total_balance

        self.session.commit()
        self.session.refresh(flags)
        return flags
