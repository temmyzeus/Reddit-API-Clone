from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(prefix="/login", tags=["Authentication"])


@router.post("/", response_model=schemas.LoginResponse)
def login_user(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> dict:
    """
    Ensure form request is a form_encoded.
    """
    user = (
        db.query(models.User)
        .filter(models.User.username == user_credentials.username)
        .first()
    )

    # if user not found
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    # if password not correct
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    token = oauth2.create_auth_token(
        data = {
            "username": user.username, 
            "password": user.password
            }
    )
    return {"access_token": token, "token_type": "bearer"}


# Forget Password
