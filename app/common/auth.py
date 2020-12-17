from datetime import datetime, timedelta
from hashlib import sha1
from typing import Optional

from fastapi import HTTPException
from fastapi import status
from jose import jwt, JWTError

from app.config import ALGORITHM

forbidden_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Unauthorized",
    headers={"WWW-Authenticate": "Bearer"},
)

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


class TokenDecodeException(Exception):
    pass


def get_hashed_password(password):
    return sha1(bytes(password + "salt", 'utf-8')).hexdigest()


def pwd_verify(plain, hashed):
    return get_hashed_password(plain) == hashed


def create_access_token(data: dict, secret_key, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token, secret_key):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise TokenDecodeException("JWTError")
