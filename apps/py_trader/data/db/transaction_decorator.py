from sqlalchemy.ext.asyncio import AsyncSession


def transactional(func, db : AsyncSession):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        db.commit()

    return wrapper

        