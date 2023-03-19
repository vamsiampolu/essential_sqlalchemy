from essential_sqlalchemy.models.customer_order import CustomerOrder, CustomerOrderList
from essential_sqlalchemy.models.order import Order, OrderList
from essential_sqlalchemy.schemas.cookies import cookies
from essential_sqlalchemy.schemas.line_items import line_items
from essential_sqlalchemy.schemas.orders import orders
from essential_sqlalchemy.schemas.users import users
from sqlalchemy.sql import func, insert, select

from sqlalchemy.engine import Connection


class Orders:
    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def insert_one(self, order: Order) -> int:
        ins = insert(orders).values(**order.dict())
        res = self.connection.execute(ins)
        return res.rowcount

    def insert_many(self, order_list: OrderList) -> int:
        ins = insert(orders)
        order_values = []
        for item in order_list:
            order_values.append(item.dict())

        ins = ins.values(order_values)
        res = self.connection.execute(ins)

        return res.rowcount

    def get_all(self) -> OrderList:
        rp = self.connection.execute(select([orders]))
        order_list = []
        for record in rp.fetchall():
            order = Order.from_orm(record)
            order_list.append(order)

        return OrderList(__root__=order_list)

    def get_orders_by_customer_name(self, customer_name: str) -> CustomerOrderList:
        columns = [
            orders.c.order_id,
            users.c.username,
            users.c.phone,
            cookies.c.cookie_name,
            line_items.c.quantity,
            line_items.c.extended_cost,
        ]

        customer_orders = select(columns)

        customer_orders = customer_orders.select_from(
            orders.join(users).join(line_items).join(cookies)
        ).where(users.c.username == customer_name)

        rp = self.connection.execute(customer_orders)

        customer_orders_list = []

        print(rp.keys())
        for record in rp.fetchall():
            item = CustomerOrder.from_orm(record)
            customer_orders_list.append(item)

        return CustomerOrderList(__root__=customer_orders_list)

    def get_order_count_per_user(self) -> list[dict]:
        columns = [users.c.username, func.count(orders.c.order_id)]

        all_orders = select(columns)
        all_orders = all_orders.select_from(users.outerjoin(orders))
        all_orders = all_orders.group_by(users.c.username)

        result = self.connection.execute(all_orders).fetchall()
        user_order_count_list: list[dict] = []

        for row in result:
            user_order_count_list.append(row._asdict())

        return user_order_count_list

    def find_orders(
        self, customer_name: str, details: bool = False
    ) -> list[CustomerOrder]:
        columns = [orders.c.order_id, users.c.username, users.c.phone]
        joins = users.join(orders)

        if details:
            columns.extend(
                [
                    cookies.c.cookie_name,
                    line_items.c.quantity,
                    line_items.c.extended_cost,
                ]
            )
            joins = joins.join(line_items).join(cookies)

        cust_orders = select(columns)
        cust_orders = cust_orders.select_from(joins)
        cust_orders = cust_orders.where(users.c.username == customer_name)

        result = self.connection.execute(cust_orders).fetchall()
        customer_orders_result = []

        for item in result:
            element = item._asdict()
            customer_orders_result.append(element)

        return customer_orders_result
