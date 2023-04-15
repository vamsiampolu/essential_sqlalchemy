import pytest

from typing import Generator
from sqlalchemy.engine import Engine, Connection

from essential_sqlalchemy.config import Config
from essential_sqlalchemy.db.engine import get_engine
from essential_sqlalchemy.db.metadata import metadata


@pytest.fixture(scope="session")
def config() -> Generator[Config, None, None]:
    Config.__config__.env_file = ".env.test"
    config = Config(DB_NAME="cookie_shop_test")
    yield config


@pytest.fixture(scope="session")
def engine(config: Config) -> Generator[Engine, None, None]:
    engine = get_engine(config)
    yield engine


@pytest.fixture(scope="session")
def connection(engine: Engine) -> Generator[Connection, None, None]:
    connection: Connection = engine.connect()
    yield connection


@pytest.fixture(scope="function", autouse=True)
def manage_tables(engine: Engine) -> Generator:
    metadata.create_all(bind=engine)
    yield metadata.tables.keys()
    print("dropping tables")
    metadata.drop_all(bind=engine)
