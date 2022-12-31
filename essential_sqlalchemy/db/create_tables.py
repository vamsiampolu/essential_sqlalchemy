from .metadata import metadata
from .engine import engine


def create_tables():
    metadata.create_all(engine)
