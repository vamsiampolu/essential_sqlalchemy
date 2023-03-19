import json
from dotenv import load_dotenv
from pydantic import parse_obj_as

from sqlalchemy.engine import Connection
from essential_sqlalchemy.crud.cookies_crud import Cookie, Cookies, CookiesMeta
from essential_sqlalchemy.crud.line_items_crud import LineItems
from essential_sqlalchemy.crud.orders_crud import Orders
from essential_sqlalchemy.crud.users_crud import Users
from essential_sqlalchemy.db.create_tables import create_tables, engine

from essential_sqlalchemy.models.line_items import LineItemList
from essential_sqlalchemy.models.customer_order import CustomerOrder, CustomerOrderList
from essential_sqlalchemy.models.order import Order
from essential_sqlalchemy.models.user import UserList
from essential_sqlalchemy.models.cookie import CookieList

from .config import Config

print("foobar")
load_dotenv()
config = Config(DB_NAME="cookie_shop")
print(config)

create_tables()

connection: Connection = engine.connect()

cookies_crud = Cookies(connection=connection)
cookies_meta = CookiesMeta(connection=connection)
users_crud = Users(connection=connection)
orders_crud = Orders(connection=connection)
line_items_crud = LineItems(connection=connection)


def dict_to_model(obj: dict) -> Cookie:
    return Cookie(**obj)


def model_to_json(
    obj: Cookie | CookieList | CustomerOrder | CustomerOrderList | Order | UserList,
) -> str:
    return obj.json()


def init_cookies() -> None:
    cookie = Cookie(
        cookie_name="chocolate chip",
        cookie_recipe_url="http://some.aweso.me/cookie/recipe.html",
        cookie_sku="CC01",
        quantity=12,
        unit_cost=0.50,
    )

    result = cookies_crud.insert_one(cookie)
    print(result)

    inventory_list = [
        {
            "cookie_name": "peanut butter",
            "cookie_recipe_url": "http://some.aweso.me/cookie/peanut.html",
            "cookie_sku": "PB01",
            "quantity": 24,
            "unit_cost": 0.25,
        },
        {
            "cookie_name": "oatmeal raisin",
            "cookie_recipe_url": "http://some.okay.me/cookie/raisin.html",
            "cookie_sku": "EWW01",
            "quantity": 100,
            "unit_cost": 1.00,
        },
    ]

    cookie_models = list(map(dict_to_model, inventory_list))
    print(cookie_models)
    cookies_crud.insert_many(cookie_models)


def init_customers() -> None:
    customer_list = [
        {
            "username": "cookiemon",
            "email_address": "mon@cookie.com",
            "phone": "111-111-1111",
            "password": "password",
        },
        {
            "username": "cakeeater",
            "email_address": "cakeeater@cake.com",
            "phone": "222-222-2222",
            "password": "password",
        },
        {
            "username": "pieguy",
            "email_address": "guy@pie.com",
            "phone": "333-333-3333",
            "password": "password",
        },
    ]

    customers = UserList.parse_obj(customer_list)
    print(users_crud.insert_many(customers))


def init_orders() -> None:
    order_one = Order(order_id=1, user_id=1)
    order_two = Order(order_id=2, user_id=2)

    print(orders_crud.insert_one(order_one))
    print(orders_crud.insert_one(order_two))


def init_line_items() -> None:
    items = [
        {"order_id": 1, "cookie_id": 1, "quantity": 2, "extended_cost": 1.00},
        {"order_id": 1, "cookie_id": 3, "quantity": 12, "extended_cost": 3.00},
        {"order_id": 2, "cookie_id": 1, "quantity": 24, "extended_cost": 12.00},
        {"order_id": 2, "cookie_id": 4, "quantity": 6, "extended_cost": 6.00},
    ]

    line_item_list = parse_obj_as(LineItemList, items)

    line_items_crud.insert_many(line_item_list)


def init_db() -> None:
    init_customers()
    init_cookies()
    init_orders()
    init_line_items()


def run_queries() -> None:
    print(orders_crud.get_orders_by_customer_name("cookiemon").json())
    print(json.dumps(orders_crud.get_order_count_per_user()))

    print(json.dumps(orders_crud.find_orders("cakeeater")))
    print(orders_crud.find_orders(customer_name="cakeeater", details=True))

    read_customers = users_crud.read_all_users()
    print(read_customers.json())

    choco_chip = cookies_crud.find_one_by_name("chocolate chip")
    print(choco_chip.json())

    best_selling_cookies = cookies_crud.get_top_n_cookies_by_quantity(2)

    print(CookieList(__root__=best_selling_cookies).json())
    print(cookies_meta.total_cookies_ordered())
    print(cookies_meta.cookie_inventory())

    cookies_with_chocolate = cookies_crud.get_cookie_with_name_like("chocolate")
    print(CookieList(__root__=cookies_with_chocolate).json())

    cookies_meta.get_inventory_cost()

    print(cookies_crud.update_cookie_by_name("chocolate chip", {"quantity": 132}))
    print(cookies_crud.remove_cookie_by_name("dark chocolate chip"))

    print(cookies_crud.remove_all())
