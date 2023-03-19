from pydantic import BaseModel
from typing import Iterator, Any


class Order(BaseModel):
    order_id: int
    user_id: int
    shipped: bool = False

    class Config:
        orm_mode = True


class OrderList(BaseModel):
    __root__: list[Order]

    def __iter__(self) -> Iterator[Order]:  # type: ignore[override]
        return iter(self.__root__)

    def __getitem__(self, item: Any) -> Any:
        return self.__root__[item]
