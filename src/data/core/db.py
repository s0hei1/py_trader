from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.tools.di.container import Container


def get_engine(db_url : str = Container.settings().database_url):
    return  create_engine(
    db_url,
    echo=True,
    future=True
)

def get_session() -> sessionmaker:
    return sessionmaker(get_engine(), expire_on_commit=False)

local_session = get_session()
def get_session() -> Session:
    return local_session()
