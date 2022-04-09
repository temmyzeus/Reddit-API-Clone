from os import access
from jose import jwt
from  datetime import datetime, timedelta

from .config import auth_config

SECRET_KEY:str = auth_config.SECRET_KEY
ALGORITHM:str = auth_config.ALGORITHM
ACCESS_TOKEN_TIMEOUT_IN_MINUTES:int = auth_config.ACCESS_TOKEN_TIMEOUT_IN_MINUTES

def create_auth_token(data: dict):
    to_encode = data.copy()
    expiration_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_TIMEOUT_IN_MINUTES)
    to_encode.update({"exp": expiration_time})

    encoded_jwt = jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

