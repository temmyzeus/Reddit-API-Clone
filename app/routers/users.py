from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas, utils
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/user", tags=["Users"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.CreateUserRequest, db: Session = Depends(get_db)):
    """
    Create a new user
    
    user: dict
        User Details
    db: Session
        Database Object

    Watch out: if username exists, if email exists
    """
    # if username exits, return error
    existing_user = (
        db.query(models.User).filter(models.User.username == user.username).first()
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="username already exists"
        )

    # if email exits, return error
    existing_email = (
        db.query(models.User).filter(models.User.email == user.email).first()
    )
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="email already exists"
        )
    
    user.password = utils.hash_password(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    return {"message": "User Created"}


@router.patch("/")
def update_user(user: schemas.UpdateUserRequest, db: Session = Depends(get_db)):
    pass
