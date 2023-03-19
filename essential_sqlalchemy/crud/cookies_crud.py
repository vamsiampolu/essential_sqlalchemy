from sqlalchemy.sql.sqltypes import Numeric
from essential_sqlalchemy.schemas.cookies import cookies
from essential_sqlalchemy.models.cookie import Cookie
from sqlalchemy.sql import cast, delete, select, func, update


def model_to_dict(item: Cookie):
    return item.dict()


class Cookies:
    def __init__(self, connection) -> None:
        self.connection = connection

    def insert_one(self, cookie: Cookie):
        ins = cookies.insert().values(**cookie.dict())
        print(str(ins))
        print(ins.compile().params)
        result = self.connection.execute(ins)
        return result.inserted_primary_key

    def insert_many(self, cookies_list: list[Cookie]):
        ins = cookies.insert()
        cookies_dict_list = map(model_to_dict, cookies_list)
        result = self.connection.execute(ins, list(cookies_dict_list))
        return result

    def get_all(self):
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

    def get_one(self):
        s = select([cookies])
        rp = self.connection.execute(s)
        result = rp.first()
        return Cookie.from_orm(result)

    def get_all_cookie_name_and_quantity(self):
        s = select([cookies.c.cookie_name, cookies.c.quantity])
        rp = self.connection.execute(s)
        print(rp.keys())
        records = rp.fetchall()
        cookie_records = []
        for record in records:
            print(f"Cookie named {record.cookie_name} in {record.quantity}")
            item = {"cookie_name": record.cookie_name, "quantity": record.quantity}
            cookie_records.append(item)
        return cookie_records

    def find_one_by_name(self, cookie_name):
        s = select([cookies]).where(cookies.c.cookie_name == cookie_name)
        rp = self.connection.execute(s)
        record = rp.first()
        return Cookie.from_orm(record)

    def get_top_n_cookies_by_quantity(self, n):
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

    def get_cookie_with_name_like(self, name):
        s = select([cookies]).where(cookies.c.cookie_name.like(f"%{name}%"))
        rp = self.connection.execute(s)
        cookie_list = []
        for record in rp.fetchall():
            item = Cookie.from_orm(record)
            cookie_list.append(item)

        return cookie_list

    def update_cookie_by_name(self, name: str, updated_values: dict):
        u = update(cookies).where(cookies.c.cookie_name == name)
        u = u.values(**updated_values)

        result = self.connection.execute(u)
        return result.rowcount

    def remove_cookie_by_name(self, name):
        u = delete(cookies).where(cookies.c.cookie_name == name)
        result = self.connection.execute(u)
        return result.rowcount

    def remove_all(self):
        u = delete(cookies)
        result = self.connection.execute(u)
        return result.rowcount


class CookiesMeta:
    def __init__(self, connection) -> None:
        self.connection = connection

    def total_cookies_ordered(self):
        s = select(func.sum(cookies.c.quantity))
        rp = self.connection.execute(s)
        return rp.scalar()

    def cookie_inventory(self):
        # By default the count columns are named count_1 and so on
        # These labels are confusing as heck, we can rename these to
        # be clear and meaningful using `label`
        s = select([func.count(cookies.c.cookie_name).label("inventory_count")])
        rp = self.connection.execute(s)
        record = rp.first()
        print(record.keys())
        return record.inventory_count

    def get_inventory_cost(self):
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
