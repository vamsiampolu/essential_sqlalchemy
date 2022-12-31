from pydantic import BaseModel, Field
from typing import *

class Cookie(BaseModel):
    cookie_id: Optional[int] = None
    cookie_name: str = Field(max_length=50)
    cookie_recipe_url: str = Field(max_length=255)
    cookie_sku: str = Field(max_length=55)
    quantity: int
    unit_cost: float

    class Config():
        orm_mode = True