from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.common.auth import decode_token, TokenDecodeException, credentials_exception
from app.common.db_init import SessionLocal, engine
from app.config import PLAYERS_API_SECRET_KEY, PUBLISHER_API_SECRET_KEY
from app.crud import auth

studio_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
players_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="players/token")


def get_db():
    db = SessionLocal(bind=engine)
    try:
        yield db
    finally:
        db.close()


async def get_current_player(db: Session = Depends(get_db),
                             token: str = Depends(players_oauth2_scheme)):
    try:
        payload = decode_token(token, PLAYERS_API_SECRET_KEY)
    except TokenDecodeException:
        raise credentials_exception
    player = auth.get_player_by_id(db, player_id=payload.get("id"))
    if player is None:
        raise credentials_exception
    return player


async def get_current_user(db: Session = Depends(get_db),
                           token: str = Depends(studio_oauth2_scheme)):
    try:
        payload = decode_token(token, PUBLISHER_API_SECRET_KEY)
    except TokenDecodeException:
        raise credentials_exception
    user = auth.get_user(db, user_id=payload.get("id"))
    if user is None:
        raise credentials_exception
    return user
