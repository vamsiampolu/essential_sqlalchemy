from essential_sqlalchemy.schemas.cookies import cookies
from essential_sqlalchemy.models.cookie import Cookie
from sqlalchemy.sql import select
from typing import List

def model_to_dict(item: Cookie): 
    item.dict()


class Cookies():
    def __init__(self, connection) -> None:
        self.connection = connection
    
    def insert_one(self, cookie: Cookie):
        ins = cookies.insert().values(**cookie.dict())
        print(str(ins))
        print(ins.compile().params)
        result = self.connection.execute(ins)
        return result.inserted_primary_key

    def insert_many(self, cookies_list: List[Cookie]):
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
            print(f'Cookie named {record.cookie_name} in {record.quantity}')
            item = {"cookie_name": record.cookie_name, "quantity": record.quantity }
            cookie_records.append(item)
        return cookie_records

    def find_one_by_name(self, cookie_name):
        s = select([cookies]).where(cookies.c.cookie_name == cookie_name)
        rp = self.connection.execute(s)
        record = rp.first()
        return Cookie.from_orm(record)