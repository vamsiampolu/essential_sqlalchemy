from datetime import datetime
from sqlalchemy import DateTime, Integer, String, Table, Column
from essential_sqlalchemy.db.metadata import metadata

users = Table(
    "users",
    metadata,
    Column("user_id", Integer(), primary_key=True),
    Column("username", String(15), nullable=False, unique=True),
    Column("email_address", String(255), nullable=False),
    Column("phone", String(20), nullable=False),
    Column("password", String(25), nullable=False),
    Column("created_at", DateTime(), default=datetime.now),
    Column("updated_at", DateTime(), default=datetime.now, onupdate=datetime.now),
)
