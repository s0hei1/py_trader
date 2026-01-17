from fastapi import Depends

from apps.paperless.data.db.db import get_db
from apps.paperless.data.repository.department_repository import DepartmentRepository
from apps.paperless.data.repository.goods_exit import GoodsExitRepository
from apps.paperless.data.repository.goods_exit_approvals import (
    GoodsExitApprovalRepository,
)
from apps.paperless.data.repository.goods_exit_docs import GoodsExitDocRepository
from apps.paperless.data.repository.user_repository import UserRepository


class RepositoryDI:

    @classmethod
    def user_repository(cls, db=Depends(get_db)) -> UserRepository:
        return UserRepository(db)

    @classmethod
    def department_repository(cls, db=Depends(get_db)) -> DepartmentRepository:
        return DepartmentRepository(db)

    @classmethod
    def goods_exit_doc_repository(cls, db=Depends(get_db)) -> GoodsExitDocRepository:
        return GoodsExitDocRepository(db)

    @classmethod
    def goods_exit_repository(cls, db=Depends(get_db)) -> GoodsExitRepository:
        return GoodsExitRepository(db)

    @classmethod
    def good_exit_approval_repository(
        cls, db=Depends(get_db)) -> GoodsExitApprovalRepository:
        return GoodsExitApprovalRepository(db)
