from sqlalchemy.engine import Engine
from .metadata import metadata


def create_tables(engine: Engine) -> None:
    metadata.create_all(engine)
