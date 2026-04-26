from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    database_url : str = ''

    @property
    def database_url_without_asyncpg(self):
        return self.database_url.replace("+asyncpg", "")


    class Config:
        env_file = Path(__file__).parent / '.env'
