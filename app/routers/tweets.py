from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db


router = APIRouter(prefix="/tweet", tags=["Tweets"])


@router.get("/", response_model=list[schemas.GetTweetResponse])
def get_tweets(db: Session = Depends(get_db)):
    """Get a list of Tweets"""
    tweets = db.query(models.Tweet).all()
    return tweets

@router.get("/{id}", response_model=schemas.GetTweetResponse)
def get_tweet(id: int, db: Session = Depends(get_db)):
    """Get single Tweet"""
    tweet = db.query(models.Tweet).filter(models.Tweet.id == id).first()
    if not tweet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tweet not found")
    return tweet

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_tweet(tweet: schemas.TweetRequest, db: Session = Depends(get_db)):
    print(tweet.dict())
    new_tweet = models.Tweet(**tweet.dict())
    db.add(new_tweet)
    db.commit()
    return {"message": "Tweet created"}

@router.patch("/")
def edit_tweet(tweet: schemas.UpdateTweetRequest, db: Session = Depends(get_db)):
    pass

@router.delete("/{id}")
def delete_tweet(id: int,  db: Session = Depends(get_db)):
    """Delete a tweet based on ID"""
    tweet = db.query(models.Tweet).filter(models.Tweet.id == id).delete()
    # tweet return 1 if deleted and 0 if is isn't deleted, i.e id not present
    if not tweet:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Tweet not found")
    db.commit()
    return {"message": "Tweet Deleted"}
