from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from . import models, schemas
from .config import auth_config
from .database import get_db

SECRET_KEY:str = auth_config.SECRET_KEY
ALGORITHM:str = auth_config.ALGORITHM
ACCESS_TOKEN_TIMEOUT_IN_MINUTES:int = auth_config.ACCESS_TOKEN_TIMEOUT_IN_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_auth_token(data: dict):
    to_encode = data.copy()
    expiration_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_TIMEOUT_IN_MINUTES)
    to_encode.update({"exp": expiration_time})

    encoded_jwt = jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_auth_token(token: str, credentials_exception):
    # if access_token isn't correct
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")

        if not username:
            raise credentials_exception
        
        token_data = schemas.TokenData(username=username)
    
    except JWTError as err_info:
        raise credentials_exception

    # How is the timeout verified
    # if payload.get("exp") > datetime.utcnow():
    #     raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail="Timeout")

    return token_data
    

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authemticate": "Bearer"}
    )
    token_data = verify_auth_token(token, credentials_exception)
    # the above logic seems enough but, if user still has acces token after deletion from database, return an error
    user = db.query(models.User).filter(models.User.username == token_data.username).first()
    if not user:
        raise  credentials_exception
    return token_data
