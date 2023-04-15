from sqlalchemy.engine import Connection

from essential_sqlalchemy.crud.line_items_crud import LineItems
from essential_sqlalchemy.models.line_items import LineItem, LineItemList


def test_insert_one_line_item(connection: Connection) -> None:
    crud = LineItems(connection)
    line_item = LineItem(order_id=3, cookie_id=3, quantity=12, extended_cost=50)

    transaction = connection.begin()
    inserted_count = crud.insert_one(line_item)
    transaction.commit()

    assert inserted_count == 1


def test_insert_many_line_items(connection: Connection) -> None:
    crud = LineItems(connection)

    line_items_list = LineItemList(
        __root__=[
            LineItem(order_id=3, cookie_id=3, quantity=12, extended_cost=50),
            LineItem(order_id=2, cookie_id=2, quantity=6, extended_cost=24),
        ]
    )

    transaction = connection.begin()
    inserted_count = crud.insert_many(line_items_list)
    transaction.commit()

    assert inserted_count == 2
