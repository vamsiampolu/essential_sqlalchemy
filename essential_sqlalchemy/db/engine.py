from sqlalchemy import create_engine
from essential_sqlalchemy.config import Config

print("Inside db.engine")
db_name = Config().DB_NAME

print(f"The {db_name} is the db to be used")
engine = create_engine(f"sqlite:///{db_name}.db", echo=True)
