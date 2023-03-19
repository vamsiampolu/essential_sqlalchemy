from pydantic import BaseSettings, Field


class Config(BaseSettings):
    DB_NAME: str = Field("name of the sqlite database")
