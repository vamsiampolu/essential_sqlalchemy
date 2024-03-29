from pydantic import BaseSettings, Field


class Config(BaseSettings):
    DB_NAME: str = Field("name of the sqlite database", env="DB_NAME")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
