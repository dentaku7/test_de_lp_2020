from typing import List

from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.common.auth import get_hashed_password
from app.common.deps import get_db, get_current_player
from app.crud import players as crud
from app.crud.players import UserIsAlreadyRegisteredException
from app.schemas.games import GameIn
from app.schemas.players import PlayerIn, PlayerGameOut, PlayerOut

router = APIRouter()


@router.get("/me", response_model=PlayerOut, status_code=status.HTTP_200_OK)
async def get_players(current_player: PlayerOut = Depends(get_current_player)):
    return current_player


@router.post("/signup", response_model=PlayerOut, status_code=status.HTTP_201_CREATED)
async def register_player(player: PlayerIn, db: Session = Depends(get_db)):
    try:
        db_player = crud.register_player(db, player.name,
                                         get_hashed_password(player.password))
        pass
    except (IntegrityError, UserIsAlreadyRegisteredException):
        raise HTTPException(status_code=400, detail="Player name was already taken")
    return db_player


@router.post("/delete", status_code=status.HTTP_200_OK)
async def delete_player(current_player: PlayerOut = Depends(get_current_player),
                        db: Session = Depends(get_db)):
    crud.delete_player(db, current_player.id)
    return {"message": "Player was deleted"}


@router.get("/games",
            response_model=List[PlayerGameOut],
            status_code=status.HTTP_200_OK)
async def get_player_games(current_player: PlayerOut = Depends(get_current_player),
                           db: Session = Depends(get_db)):
    return crud.get_player_games(db, current_player)


@router.post("/games/register",
             response_model=PlayerGameOut,
             status_code=status.HTTP_201_CREATED)
async def player_register_game(game: GameIn,
                               current_player: PlayerOut = Depends(get_current_player),
                               db: Session = Depends(get_db)):
    try:
        ret = crud.player_register_game(db, current_player, game)
    except IntegrityError:
        db.rollback()
        ret = crud.get_player(db, current_player)
    return ret


@router.post("/games/unregister",
             response_model=PlayerGameOut,
             status_code=status.HTTP_200_OK)
async def player_unregister_game(game: GameIn,
                                 current_player: PlayerOut = Depends(get_current_player),
                                 db: Session = Depends(get_db)):
    return crud.player_unregister_game(db, current_player, game)
