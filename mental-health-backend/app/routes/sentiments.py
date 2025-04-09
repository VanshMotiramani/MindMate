from fastapi import FastAPI, Depends, status, HTTPException, APIRouter, Request
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, oauth2
from ..database import get_db
# from ..ml_model import get_recommendation
from ..recommender import get_comprehensive_support


router = APIRouter(
    prefix="/sentiments",
    tags=["Sentiment Analysis"]
)

@router.get("/", response_model=List[schemas.SentimentResponse])
def get_sentiments(request: Request, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    try:
        all_sentiments = db.query(models.Sentiment).filter(models.Sentiment.owner_id == current_user.id).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error retrieving sentiments: {str(e)}")

    return [
        schemas.SentimentResponse(
            id=s.id,
            sentiments=s.sentiments,
            recommendation=s.recommendation,
            owner=schemas.UserResponse(
                id=s.owner.id,
                email=s.owner.email
            )
        ) for s in all_sentiments
    ]

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.SentimentResponse)
def create_sentiment(sentiments: schemas.CreateSentiment, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):

    result = get_comprehensive_support(sentiments.sentiments)
    
    new_sentiment = models.Sentiment(
        sentiments=sentiments.sentiments,
        recommendation=result,  # full dict
        owner_id=current_user.id
    )
    db.add(new_sentiment)
    db.commit()
    db.refresh(new_sentiment)

    return schemas.SentimentResponse(
        id=new_sentiment.id,
        sentiments=new_sentiment.sentiments,
        recommendation=new_sentiment.recommendation,
        owner=schemas.UserResponse(
            id=current_user.id,
            email=current_user.email
        )
    )

@router.get("/{id}", response_model=schemas.SentimentResponse)
def get_sentiment(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    user_sentiment = db.query(models.Sentiment).filter(models.Sentiment.id == id).first()
    if not user_sentiment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sentiment with id {id} not found")
    
    if user_sentiment.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this sentiment")
    
    return user_sentiment

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sentiment(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    sentiment_query = db.query(models.Sentiment).filter(models.Sentiment.id == id)
    sentiment = sentiment_query.first()

    if not sentiment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sentiment with id {id} not found")
    
    if sentiment.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this sentiment")
    
    sentiment_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Sentiment deleted successfully"}

@router.put("/", response_model=schemas.SentimentResponse)
def update_sentiments(
    sentiment_data: schemas.CreateSentiment,
    db: Session = Depends(get_db),
    current_user = Depends(oauth2.get_current_user)
):
    existing_sentiment = db.query(models.Sentiment).filter(
        models.Sentiment.owner_id == current_user.id
    ).order_by(models.Sentiment.id.desc()).first()

    if not existing_sentiment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No sentiment record found for user {current_user.id}")

    existing_sentiment.sentiments = sentiment_data.sentiments  
    db.commit()
    db.refresh(existing_sentiment)

    return schemas.SentimentResponse(
        id=existing_sentiment.id,
        sentiments=existing_sentiment.sentiments,
        recommendation="new_recommendation",
        owner=schemas.UserResponse(
            id=existing_sentiment.owner.id,
            email=current_user.email
        )
    )
