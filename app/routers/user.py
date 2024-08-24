from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schema, utils
from .. database import get_db

router = APIRouter(
    prefix= "/user/api/v1",
    tags = ["Users"],
)
#craete user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.UserResponse)
def create_user(user: schema.UserCreate,  db: Session = Depends(get_db)):
    # hash the password - user provided
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())  # Convert Pydantic model to SQLAlchemy model
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # Update the post with the newly created id and return it
    return new_user

@router.get("/{user_id}", response_model=schema.UserResponse) 
def get_user(user_id:int ,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id:{user_id} does not exist")
    return user