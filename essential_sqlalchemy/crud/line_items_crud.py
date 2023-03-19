from sqlalchemy.sql import insert
from essential_sqlalchemy.schemas.line_items import line_items
from essential_sqlalchemy.models.line_items import LineItem, LineItemList


class LineItems:
    def __init__(self, connection) -> None:
        self.connection = connection

    def insert_one(self, value: LineItem) -> int:
        ins = insert(line_items).values(**value.dict())
        res = self.connection.execute(ins)
        return res.rowcount

    def insert_many(self, arr: LineItemList) -> int:
        ins = insert(line_items)
        values = []

        for item in arr:
            values.append(item.dict())

        ins = ins.values(values)

        res = self.connection.execute(ins)
        return res.rowcount
