from typing import Optional

from pydantic import BaseModel

from . import BaseModelORM


class GameIn(BaseModel):
    id: Optional[int]
    name: Optional[str]


class GameNameIn(BaseModel):
    name: str


class StudioName(BaseModelORM):
    name: str


class GameOut(BaseModelORM):
    id: int
    name: str
    studio: StudioName
