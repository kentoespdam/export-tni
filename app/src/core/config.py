from pydantic import MySQLDsn
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore",
    )

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    COKLIT_DB_NAME: str
    DB_USER: str
    DB_PASS: str
    SQUIDS_ALPHABET: str = "Asd"
    SQUIDS_MIN_LENGTH: int
    ALLOWED_ORIGINS: list[str]

    @property
    def SQLALCHEMY_DATABASE_URL(self):
        return MultiHostUrl.build(
            scheme="mysql+pymysql",
            host=self.DB_HOST,
            port=self.DB_PORT,
            username=self.DB_USER,
            password=self.DB_PASS,
            path=self.DB_NAME,
        )

    @classmethod
    def get_mysql_dsn(cls):
        return MySQLDsn.build(
            scheme="mysql+pymysql",
            host=cls.DB_HOST,
            port=cls.DB_PORT,
            username=cls.DB_USER,
            password=cls.DB_PASS,
            path=cls.DB_NAME,
        )

    @property
    def COKLIT_DATABASE_URL(self):
        return MultiHostUrl.build(
            scheme="mysql+pymysql",
            host=self.DB_HOST,
            port=self.DB_PORT,
            username=self.DB_USER,
            password=self.DB_PASS,
            path=self.COKLIT_DB_NAME,
        )


settings = Settings()
