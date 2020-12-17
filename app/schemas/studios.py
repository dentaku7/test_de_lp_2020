from typing import List, Optional

from pydantic import BaseModel

from . import BaseModelORM


class StudioIn(BaseModel):
    id: Optional[int]
    name: Optional[str]


class GameOut(BaseModelORM):
    id: int
    name: str


class StudioNameOut(BaseModelORM):
    name: str


class StudioOut(StudioNameOut):
    id: int


class StudioGamesOut(StudioOut):
    games: List[GameOut]


class GamesPopularity(GameOut):
    players_count: int


class GamesWithStudioPopularity(GamesPopularity):
    players_count: int

    studio: StudioOut
