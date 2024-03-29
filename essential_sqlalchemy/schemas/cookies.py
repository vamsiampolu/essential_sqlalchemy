from essential_sqlalchemy.db.metadata import metadata
from sqlalchemy import CheckConstraint, Column, Integer, Numeric, String, Table

cookies = Table(
    "cookies",
    metadata,
    Column("cookie_id", Integer(), primary_key=True),
    Column("cookie_name", String(50), index=True),
    Column("cookie_recipe_url", String(255)),
    Column("cookie_sku", String(55)),
    Column("quantity", Integer(), nullable=False),
    Column("unit_cost", Numeric(12, 2)),
    CheckConstraint("quantity > 0", name="quantity_positive"),
)
