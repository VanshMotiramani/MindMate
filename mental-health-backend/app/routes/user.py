
from fastapi import  Depends, status, HTTPException, APIRouter
from pydantic import EmailStr
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):

    try:

        hashed_pwd = utils.hash(user.password)
        user.password = hashed_pwd

        new_user = models.Users(
            email = user.email, password = user.password
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "id": new_user.id,
            "email": new_user.email
        }
    
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Email already exists")
    
@router.get("/{email}", response_model=schemas.UserResponse)
def get_user(email: EmailStr, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.email == email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {email} not found")
    
    return {
        "id": user.id,
        "email": user.email
    }
