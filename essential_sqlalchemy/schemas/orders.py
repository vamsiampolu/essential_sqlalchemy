from essential_sqlalchemy.db.metadata import metadata
from sqlalchemy import Boolean, Column, ForeignKey, Integer, Table

orders = Table(
    "orders",
    metadata,
    Column("order_id", Integer(), primary_key=True),
    Column("user_id", ForeignKey("users.user_id")),
    Column("shipped", Boolean(), default=False),
)
