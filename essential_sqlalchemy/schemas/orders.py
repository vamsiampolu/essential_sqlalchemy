from sqlalchemy import Boolean, Column, ForeignKey
from sqlalchemy import Table, Column, Integer
from essential_sqlalchemy.db.metadata import metadata

orders = Table(
    "orders",
    metadata,
    Column("order_id", Integer(), primary_key=True),
    Column("user_id", ForeignKey("users.user_id")),
    Column("shipped", Boolean(), default=False)
)
