from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ...app import models, schemas
from ..database import get_db
from ..utils import hashing, token

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/signup", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered!")
    
    hashed_pw = hashing.hash_password(user.password)
    new_user = models.User(username = user.username, email = user.email, hashed_password = hashed_pw)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: schemas.UserCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    if not user or not hashing.verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = token.create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}