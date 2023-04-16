from essential_sqlalchemy.crud.orders_crud import Orders
from essential_sqlalchemy.models.order import Order, OrderList

from sqlalchemy.engine import Connection


def test_insert_one_order(connection: Connection) -> None:
    orders = Orders(connection)
    order = Order(order_id=1, user_id=1, shipped=False)

    transaction = connection.begin()
    inserted_count = orders.insert_one(order)
    transaction.commit()

    assert inserted_count == 1


def test_insert_many_orders(connection: Connection) -> None:
    orders = Orders(connection)

    order_list = OrderList(
        __root__=[
            Order(order_id=1, user_id=1, shipped=False),
            Order(order_id=2, user_id=3, shipped=True),
        ]
    )

    transaction = connection.begin()
    inserted_count = orders.insert_many(order_list)
    transaction.commit()

    assert inserted_count == 2


def test_get_all_orders(connection: Connection) -> None:
    orders = Orders(connection)

    order_list = OrderList(
        __root__=[
            Order(order_id=1, user_id=1, shipped=False),
            Order(order_id=2, user_id=3, shipped=True),
        ]
    )

    transaction = connection.begin()
    orders.insert_many(order_list)
    transaction.commit()

    all_orders = orders.get_all()

    assert all_orders == order_list


def test_get_all_orders_no_records(connection: Connection) -> None:
    orders = Orders(connection)
    assert orders.get_all() == OrderList(__root__=[])
