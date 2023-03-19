from pydantic import BaseModel
from typing import List


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
