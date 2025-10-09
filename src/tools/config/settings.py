from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    database_url : str = ''

    @property
    def database_url_without_psycopg2(self):
        return self.database_url.replace("+psycopg2", "")


    class Config:
        env_file = r'C:\Users\m.rahimi\PycharmProjects\py_trader\src\tools\config\.env'
