from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix="/tweet", tags=["Tweets"])


@router.get("/", response_model=list[schemas.GetTweetResponse])
def get_tweets(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    """Get a list of Tweets"""
    tweets = db.query(models.Tweet).all()
    return tweets


@router.get("/{id}", response_model=schemas.GetTweetResponse)
def get_tweet(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    """Get single Tweet with specific ID"""
    tweet = db.query(models.Tweet).filter(models.Tweet.id == id).first()
    if not tweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Tweet {id} not found"
        )
    return tweet


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_tweet(tweet: schemas.TweetRequest, db: Session = Depends(get_db), current_user= Depends(oauth2.get_current_user)):
    new_tweet = models.Tweet(username=current_user.username, **tweet.dict())
    db.add(new_tweet)
    db.commit()
    db.refresh(new_tweet)
    return new_tweet


@router.patch("/{id}")
def edit_tweet(
    id: int, tweet: schemas.UpdateTweetRequest, db: Session = Depends(get_db), current_user= Depends(oauth2.get_current_user)
):
    get_original_tweet_query = db.query(models.Tweet).filter(models.Tweet.id == id)
    original_tweet = get_original_tweet_query.first()

    # if tweet not found
    if not original_tweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tweet not found"
        )
    
    # if tweet found check if user can edit it
    if original_tweet.username != current_user.username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")

    new_tweet_update = {
        key: value if (value is not None) else original_tweet.__dict__[key]
        for key, value in tweet.dict().items()
    }
    tweet = tweet.dict()
    tweet["username"] = current_user.username
    get_original_tweet_query.update(tweet, synchronize_session=False)
    db.commit()
    return {"message": f"Tweet {id} edited."}


@router.delete("/{id}")
def delete_tweet(id: int, db: Session = Depends(get_db), current_user= Depends(oauth2.get_current_user)):
    """Delete a tweet based on ID"""
    get_original_tweet_query = db.query(models.Tweet).filter(models.Tweet.id == id)
    original_tweet = get_original_tweet_query.first()

    # if tweet not found
    if not original_tweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tweet not found"
        )

    # if tweet found, check if user can delete it
    if original_tweet.username != current_user.username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")

    get_original_tweet_query.delete(synchronize_session=False)
    db.commit()
    return {"message": f"Tweet {id} Deleted"}
