from .engine import engine
from .metadata import metadata


def create_tables() -> None:
    metadata.create_all(engine)
