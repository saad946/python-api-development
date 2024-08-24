from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from datetime import datetime, timedelta
from .. import schema, database, models
from .. database import get_db
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
#secret_key
#algorithm
#expiration time

SECRET_KEY = "asdas6dsf7fg87khjgh8787gfhcvbfdgdsdxzvxcvbrwerewthgj877675"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire}) # add expiration time to token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str,credentials_exception):

    try:  
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            id: str = payload.get("user_id") 
        
            if id is None:
                raise credentials_exception("Invalid credentials")
            token_data = schema.TokenData(id=id) #it is used to hold user data
    except JWTError:
         raise credentials_exception
    
    return token_data #user_id is returned if token is valid and has user_id in it. Otherwise, it raises an exception
            
    
def get_current_user(token: str = Depends(oauth2_scheme),  db: Session = Depends(get_db)):
     
     credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
     token_data = verify_access_token(token, credentials_exception)
     user = db.query(models.User).filter(models.User.id == token_data.id).first()
     if not user:
          raise credentials_exception



     return user


    

