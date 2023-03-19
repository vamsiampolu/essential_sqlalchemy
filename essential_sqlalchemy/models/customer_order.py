from typing import List

from pydantic import BaseModel


class CustomerOrder(BaseModel):
    order_id: int
    username: str
    phone: str
    cookie_name: str
    quantity: int
    extended_cost: float

    class Config:
        orm_mode = True


class CustomerOrderList(BaseModel):
    __root__: List[CustomerOrder]
