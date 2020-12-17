from typing import List

from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.common.auth import forbidden_exception
from app.common.deps import get_db, get_current_user
from app.config import AUTH_ROLES
from app.crud import studios as crud
from app.crud.common import UserNotFound
from app.models.users import User
from app.schemas.games import GameOut, GameNameIn
from app.schemas.players import GamePlayersOut, PlayerGameIn
from app.schemas.studios import GamesPopularity, StudioGamesOut, StudioOut

router = APIRouter()


def role_studio(current_user: User = Depends(get_current_user)):
    if current_user.role == AUTH_ROLES['studio_owner']:
        return current_user
    else:
        raise forbidden_exception


@router.get("/me", response_model=StudioOut, status_code=status.HTTP_200_OK)
async def get_studio(db: Session = Depends(get_db),
                     current_user: User = Depends(role_studio)):
    return crud.get_studio(db, current_user.studio_id)


@router.get("/games", response_model=StudioGamesOut, status_code=status.HTTP_200_OK)
async def get_studio(db: Session = Depends(get_db),
                     current_user: User = Depends(role_studio)):
    return crud.get_studio(db, current_user.studio_id)


@router.post("/games/add", response_model=GameOut, status_code=status.HTTP_201_CREATED)
async def add_game(game: GameNameIn,
                   db: Session = Depends(get_db),
                   current_user: User = Depends(role_studio)):
    try:
        db_studio = crud.studio_add_game(db, current_user, game)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Game with that name was already registered")
    return db_studio


@router.get("/games/popularity", response_model=List[GamesPopularity],
            status_code=status.HTTP_200_OK)
async def get_games_popularity(db: Session = Depends(get_db),
                               current_user: User = Depends(role_studio)):
    ret = [{
        "id": g.id,
        "name": g.name,
        "players_count": g.players_count,
    } for g in crud.get_studio_games_popularity(db, current_user.studio_id)]

    return ret


@router.get("/players", response_model=List[GamePlayersOut], status_code=status.HTTP_200_OK)
async def get_players(db: Session = Depends(get_db),
                      current_user: User = Depends(role_studio)):
    return [{"game_id": g.id, "game_name": g.name, "players": g.players}
            for g in crud.get_studio_players(db, current_user.studio_id)]


@router.post("/players/register",
             response_model=GamePlayersOut,
             status_code=status.HTTP_201_CREATED)
async def register_player(pg: PlayerGameIn,
                          db: Session = Depends(get_db),
                          current_user: User = Depends(role_studio)):
    if pg.game_id not in [g.id for g in current_user.studio.games]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid input")
    try:
        db_game = crud.studio_game_register_player(db, pg)
    except UserNotFound:
        raise HTTPException(status_code=400, detail="Invalid input")
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Already registered")
    return {"game_id": db_game.id, "game_name": db_game.name,
            "players": [p for p in db_game.players
                        if p.id == pg.player_id]}


@router.post("/players/unregister",
             response_model=GamePlayersOut,
             status_code=status.HTTP_201_CREATED)
async def unregister_player(pg: PlayerGameIn,
                            db: Session = Depends(get_db),
                            current_user: User = Depends(role_studio)):
    if pg.game_id not in [g.id for g in current_user.studio.games]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid input")
    db_game = crud.studio_game_unregister_player(db, pg)
    return {"game_id": db_game.id, "game_name": db_game.name, "players": []}
