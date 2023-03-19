from pydantic import BaseModel


class Order(BaseModel):
    order_id: int
    user_id: int
    shipped: bool = False

    class Config:
        orm_mode = True


class OrderList(BaseModel):
    __root__: list[Order]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]
