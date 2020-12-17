from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from app.common.auth import forbidden_exception
from app.common.deps import get_db, get_current_user
from app.config import AUTH_ROLES
from app.crud import publisher as crud
from app.models.users import User
from app.schemas.players import GamePlayersOut
from app.schemas.studios import GamesWithStudioPopularity
from app.schemas.users import UserOut

router = APIRouter()


def role_publisher(current_user: User = Depends(get_current_user)):
    if current_user.role == AUTH_ROLES['publisher']:
        return current_user
    else:
        raise forbidden_exception


@router.get("/me", response_model=UserOut, status_code=status.HTTP_200_OK)
async def get_publisher(current_user: User = Depends(role_publisher)):
    return current_user


@router.get("/games/popularity", response_model=List[GamesWithStudioPopularity],
            status_code=status.HTTP_200_OK)
async def get_games_popularity(db: Session = Depends(get_db),
                               current_user: User = Depends(role_publisher)):
    ret = [{
        "id": g.id,
        "name": g.name,
        "players_count": g.players_count,
        "studio": {
            "id": g.studio_id,
            "name": g.studio_name
        }
    } for g in crud.get_games_popularity(db)]
    return ret


@router.get("/studio/players", response_model=List[GamePlayersOut], status_code=status.HTTP_200_OK)
async def get_players(studio_id: int = None,
                      studio_name: str = None,
                      db: Session = Depends(get_db),
                      current_user: User = Depends(get_publisher)):
    return [{"game_id": g.id, "game_name": g.name, "players": g.players}
            for g in crud.get_studio_players(db, studio_id, studio_name)]
