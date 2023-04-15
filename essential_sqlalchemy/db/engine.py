from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from essential_sqlalchemy.config import Config


def get_engine(config: Config) -> Engine:
    db_name = config.DB_NAME
    print(f"The {db_name} is the db to be used")
    engine = create_engine(f"sqlite:///{db_name}.db", echo=True)
    return engine
