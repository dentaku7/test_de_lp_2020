from pydantic import BaseModel

from . import BaseModelORM


class UserBase(BaseModel):
    username: str


class UserIn(UserBase):
    id: int
    username: str
    studio_id: int


class UserOut(BaseModelORM):
    id: int
    username: str
    role: int
