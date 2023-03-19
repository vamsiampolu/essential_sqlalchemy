from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.sql.sqltypes import Integer, Numeric
from essential_sqlalchemy.db.metadata import metadata

line_items = Table(
    "line_items",
    metadata,
    Column("line_items_id", Integer(), primary_key=True),
    Column("order_id", ForeignKey("orders.order_id")),
    Column("cookie_id", ForeignKey("cookies.cookie_id")),
    Column("quantity", Integer()),
    Column("extended_cost", Numeric(12, 2)),
)
