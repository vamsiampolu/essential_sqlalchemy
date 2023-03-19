from sqlalchemy.sql import insert, select
from essential_sqlalchemy.models.user import User, UserList
from essential_sqlalchemy.schemas import users


class Users:
    def __init__(self, connection) -> None:
        self.connection = connection

    def insert_one(self, user: User) -> int:
        ins = insert(users).values(**user.dict())
        res = self.connection.execute(ins)
        return res.rowcount

    def insert_many(self, user_list: UserList) -> int:
        ins = insert(users)
        user_values = []
        for item in user_list:
            user_values.append(item.dict())

        ins = ins.values(user_values)
        res = self.connection.execute(ins)

        return res.rowcount

    def read_all_users(self):
        s = select([users])
        rp = self.connection.execute(s)
        user_list = []
        for row in rp.fetchall():
            item = User.from_orm(row)
            user_list.append(item)

        return UserList(__root__=user_list)
