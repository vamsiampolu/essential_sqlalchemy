from datetime import datetime

from essential_sqlalchemy.db.metadata import metadata
from sqlalchemy import Column, DateTime, Integer, String, Table

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
