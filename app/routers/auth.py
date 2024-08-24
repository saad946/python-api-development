from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. database import get_db
from .. import models, schema,utils
from .  import oauth2

router = APIRouter(
    tags= ["auth"],
)

@router.post('/login', response_model=schema.TokenResponse)
# def login(user_credentials:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
def login(user_credentials:schema.UserLogin, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not found")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect password")
    assess_token = oauth2.create_access_token(data={"user_id": user.id, "email": user.email})
    #create a JWT token
    return {"access_token": assess_token, "token_type": "bearer"}






    





