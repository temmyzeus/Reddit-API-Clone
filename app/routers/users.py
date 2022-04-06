from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/user", tags=["Users"])

@router.post("/")
def create_user(user: schemas.CreateUserRequest, db: Session = Depends(get_db)):
    """Create a new user
    
    user: dict
        user bs
    db: Session
        Database object

    Watch out: if username exists, if email exists
    """
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="username already exists")

    existing_email = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="email already exists")
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    return {"message": "User Created"}


@router.patch("/")
def update_user(user: schemas.UpdateUserRequest, db: Session = Depends(get_db)):
    pass
