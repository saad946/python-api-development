from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List
from .. import models, schema, utils
from .. database import get_db
from . import oauth2

router = APIRouter(
    prefix= "/post/api/v1",
    tags = ["Posts"],
)

@router.get("/",response_model=List[schema.PostResponse]) #Endpoint to get all posts in a list
def get_posts(db: Session = Depends(get_db),limit: int = 10):
    print(limit)
    post = db.query(models.Post).all()
    return post

# create post 
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.PostResponse)
def create_post(post: schema.PostCreate, db: Session = Depends(get_db), response_model=Response, current_user: int = Depends(oauth2.get_current_user)):
    print(current_user.email)
    new_post = models.Post(**post.dict())  # Convert Pydantic model to SQLAlchemy model,
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # Update the post with the newly created id and return it
    return new_post

#get post by id
@router.get("/{post_id}", response_model=schema.PostResponse) 
def get_post(post_id: int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id,models.Post.user_id == current_user.id).first() 

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{post_id} not found")
    return post

#delete post
@router.delete("/{post_id}")  # Endpoint with a parameter called post_id
def delete_post(post_id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{post_id} not found")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to delete this post")

    post_query.delete(synchronize_session=False) 
    db.commit() 

    return {"message": "Post deleted successfully"}



#update post
@router.post("/{post_id}",response_model=schema.PostResponse) # Endpoint with a parameter called post_id
def update_post(post_id: int, updated_post: schema.PostCreate, response_model: Response, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    update_post = db.query(models.Post).filter(models.Post.id == post_id)
    post = update_post.first()

    if post == None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post WITH id:{post_id} not exists")
    
    if post.user_id != current_user.id:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to delete this post")
    
    update_post.update(updated_post.dict(), synchronize_session=False)  # Use synchronize_session=False to avoid flushing the session after updating the post
    db.commit()
    return update_post.first()  # Return the updated post