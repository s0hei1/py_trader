from requests import Session
from sqlalchemy import select


from apps.py_trader.data.models.models import Config


class ConfigRepo:

    def __init__(self, session: Session):
        self.session = session


    def get_config(self):

        q = select(Config).order_by(Config.creation_datetime)

        pass
