from fastapi import Depends

from apps.paperless.business.service.auth_service import AuthService
from apps.paperless.business.service.goods_exit_doc_sevice import GoodsExitDocService
from apps.paperless.data.db.db import get_read_only_db
from apps.paperless.di import GeneralDI


class ServiceDI:

    @classmethod
    def auth_service(cls, db=Depends(get_read_only_db)) -> AuthService:
        return AuthService(db=db)

    @classmethod
    def goods_exit_doc_service(
        cls, db=Depends(get_read_only_db)
    ) -> GoodsExitDocService:
        return GoodsExitDocService(db=db)
