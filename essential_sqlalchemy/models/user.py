from datetime import datetime
from typing import List, Optional, Iterator, Any

from pydantic import BaseModel, Field


class User(BaseModel):
    user_id: Optional[int] = None
    username: str = Field(type=str, description="Username")
    email_address: str = Field(type=str, description="Email Address")
    phone: str = Field(type=str, description="Phone Number")
    password: str = Field(type=str, description="Password")
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="Created At Date and Time",
        type=datetime,
    )
    updated_at: datetime = Field(
        default_factory=datetime.now,
        description="Date and Time when the user was last updated",
        type=datetime,
    )

    class Config:
        orm_mode = True


class UserList(BaseModel):
    __root__: List[User]

    def __iter__(self) -> Iterator[User]:  # type: ignore[override]
        iter(self.__root__)
        return iter(self.__root__)

    def __getitem__(self, item: Any) -> Any:
        return self.__root__[item]
