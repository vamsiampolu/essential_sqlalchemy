from essential_sqlalchemy.models.cookie import Cookie
from essential_sqlalchemy.schemas.cookies import cookies
from sqlalchemy.sql import cast, delete, func, select, update
from sqlalchemy.sql.sqltypes import Numeric

from typing import TypedDict, cast as type_cast
from sqlalchemy.engine import Connection, CursorResult, Row


class CookieLabel(TypedDict):
    cookie_name: str
    quantity: int


def model_to_dict(item: Cookie) -> dict:
    return item.dict()


class Cookies:
    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def insert_one(self, cookie: Cookie) -> Row:
        ins = cookies.insert().values(**cookie.dict())
        print(str(ins))
        print(ins.compile().params)
        result = self.connection.execute(ins)
        print(result)
        return result.inserted_primary_key

    def insert_many(self, cookies_list: list[Cookie]) -> CursorResult:
        ins = cookies.insert()
        cookies_dict_list = map(model_to_dict, cookies_list)
        result = self.connection.execute(ins, list(cookies_dict_list))
        return result

    def get_all(self) -> list[Cookie]:
        s = select([cookies])
        rp = self.connection.execute(s)
        result = rp.fetchall()
        cookie_records = []
        for record in result:
            print(record.cookie_name)
            item = Cookie.from_orm(record)
            print(item)
            cookie_records.append(item)
        return cookie_records

    def get_one(self) -> Cookie:
        s = select([cookies])
        rp = self.connection.execute(s)
        result = rp.first()
        return Cookie.from_orm(result)

    def get_all_cookie_name_and_quantity(self) -> list[CookieLabel]:
        s = select([cookies.c.cookie_name, cookies.c.quantity])
        rp = self.connection.execute(s)
        print(rp.keys())
        records = rp.fetchall()
        cookie_records = []
        for record in records:
            print(f"Cookie named {record.cookie_name} in {record.quantity}")
            item: CookieLabel = {
                "cookie_name": record.cookie_name,
                "quantity": record.quantity,
            }
            cookie_records.append(item)
        return cookie_records

    def find_one_by_name(self, cookie_name: str) -> Cookie:
        s = select([cookies]).where(cookies.c.cookie_name == cookie_name)
        rp = self.connection.execute(s)
        record = rp.first()
        return Cookie.from_orm(record)

    def get_top_n_cookies_by_quantity(self, n: int) -> list[Cookie]:
        s = select([cookies])
        s = s.order_by(cookies.c.quantity)
        s = s.limit(n)

        rp = self.connection.execute(s)
        records = rp.fetchall()

        cookie_records = []
        for record in records:
            item = Cookie.from_orm(record)
            cookie_records.append(item)

        return cookie_records

    def get_cookie_with_name_like(self, name: str) -> list[Cookie]:
        s = select([cookies]).where(cookies.c.cookie_name.like(f"%{name}%"))
        rp = self.connection.execute(s)
        cookie_list: list[Cookie] = []
        for record in rp.fetchall():
            item = Cookie.from_orm(record)
            cookie_list.append(item)

        return cookie_list

    def update_cookie_by_name(self, name: str, updated_values: dict) -> int:
        u = update(cookies).where(cookies.c.cookie_name == name)
        u = u.values(**updated_values)

        result = self.connection.execute(u)
        return result.rowcount

    def remove_cookie_by_name(self, name: str) -> int:
        u = delete(cookies).where(cookies.c.cookie_name == name)
        result = self.connection.execute(u)
        return result.rowcount

    def remove_all(self) -> int:
        u = delete(cookies)
        result = self.connection.execute(u)
        return result.rowcount


class CookiesMeta:
    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def total_cookies_ordered(self) -> int:
        s = select(func.sum(cookies.c.quantity))
        rp = self.connection.execute(s)
        return type_cast(int, rp.scalar())

    def cookie_inventory(self) -> int:
        # By default the count columns are named count_1 and so on
        # These labels are confusing as heck, we can rename these to
        # be clear and meaningful using `label`
        s = select([func.count(cookies.c.cookie_name).label("inventory_count")])
        rp = self.connection.execute(s)
        record = rp.first()

        if record is not None:
            print(record.keys())
            return type_cast(int, record.inventory_count)
        else:
            return 0

    def get_inventory_cost(self) -> None:
        s = select(
            [
                cookies.c.cookie_name,
                cast((cookies.c.quantity * cookies.c.unit_cost), Numeric(12, 2)).label(
                    "inventory_cost"
                ),
            ]
        )
        rp = self.connection.execute(s)

        for row in rp.fetchall():
            print(f"{row.cookie_name} - {row.inventory_cost}")
