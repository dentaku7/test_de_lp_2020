from typing import List

from pydantic import BaseModel

from app.schemas.games import GameOut
from . import BaseModelORM


class PlayerIn(BaseModel):
    name: str
    password: str


class PlayerOut(BaseModelORM):
    id: int
    name: str


class PlayerGameIn(BaseModel):
    player_id: int
    game_id: int


class PlayerGameOut(BaseModelORM):
    name: str
    games: List[GameOut]


class GamePlayersOut(BaseModel):
    game_id: int
    game_name: str

    players: List[PlayerOut]

    class Config:
        orm_mode = True
