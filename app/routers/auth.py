from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.config import ACCESS_TOKEN_EXPIRE_MINUTES, PUBLISHER_API_SECRET_KEY, PLAYERS_API_SECRET_KEY
from app.crud import auth as crud
from app.common.auth import (
    pwd_verify,
    create_access_token,
    credentials_exception
)
from app.common.deps import get_db

auth_router = APIRouter()


@auth_router.post("/login")
async def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    db_user = crud.get_user_by_name(db, form_data.username)
    if not db_user or not pwd_verify(form_data.password, db_user.password):
        raise credentials_exception
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"id": db_user.id},
        expires_delta=access_token_expires,
        secret_key=PUBLISHER_API_SECRET_KEY
    )
    return {"access_token": access_token, "token_type": "bearer"}


players_router = APIRouter()


@players_router.post("/token")
async def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    db_player = crud.get_player_by_name(db, form_data.username)
    if not db_player or not pwd_verify(form_data.password, db_player.password):
        raise credentials_exception
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"id": db_player.id},
        expires_delta=access_token_expires,
        secret_key=PLAYERS_API_SECRET_KEY
    )
    return {"access_token": access_token, "token_type": "bearer"}
