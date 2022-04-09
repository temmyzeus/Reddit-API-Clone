from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(prefix="/user", tags=["Users"])


@router.get("/")
def get_users(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    users = db.query(models.User).all()
    return users


@router.get("/{username}")
def get_user(username: str, db: Session = Depends(get_db), current_user= Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.username == username).first()
    return user


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


@router.patch("/", status_code=status.HTTP_201_CREATED)
def update_user(user_update_info: schemas.UpdateUserRequest, db: Session = Depends(get_db), current_user= Depends(oauth2.get_current_user)):
    """
    Update User info
    """
    update_user_query = db.query(models.User).filter(models.User.username == current_user.username)
    user = update_user_query.first()

    # To Do: Implement Password Change Logic
    # P.S checking if user exists seem crazy since user is gotten from current_user, but doesn't  hurt
    # since it should never be trigerred 
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User: {current_user.username} not Found")
    
    updated_user = {
        key: value if (value is not None) else user.__dict__[key]
        for key, value in user_update_info.dict().items()
    }
    
    update_user_query.update(updated_user, synchronize_session=False)
    db.commit()
    return updated_user

    pass
