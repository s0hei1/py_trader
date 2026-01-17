from sqlalchemy.ext.asyncio import AsyncSession


class ReadOnlyAsyncSession(AsyncSession):

    async def add(self, instance: object, _warn: bool = True) -> None:
        raise PermissionError("Read only session does not support add")

    async def delete(self, instance: object, _warn: bool = True) -> None:
        raise PermissionError("Read only session does not support delete")

    async def flush(self, _warn: bool = True) -> None:
        raise PermissionError("Read only session does not support flush")

    async def commit(self) -> None:
        raise PermissionError("Read only session does not support commit")

    async def rollback(self) -> None:
        raise PermissionError("Read only session does not support rollback")
