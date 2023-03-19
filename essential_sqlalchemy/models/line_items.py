from pydantic import BaseModel, Field
from typing import List


class LineItem(BaseModel):
    order_id: int = Field(description="Order Id")
    cookie_id: int = Field(description="Cookie Id")
    quantity: int = Field(description="Quantity")
    extended_cost: int = Field(description="Extended Cost")

    class Config:
        orm_mode = True


class LineItemList(BaseModel):
    __root__: List[LineItem]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]
