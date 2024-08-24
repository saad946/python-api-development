from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class PostBase(BaseModel): # Define a Pydantic model for the POST data so it can be validated 
    title: str
    content: str
    category: int = 1  # Default value is 1 for unpublished posts and unentered data
    published: bool
    rating: Optional[float] = None
    user_id: int 


class PostCreate(PostBase): # Define a Pydantic model for creating a new post
    pass

class UserResponse(BaseModel): # Define a Pydantic model for the response when getting a post
    created_at: datetime
    id: int
    email: EmailStr
    class config: #it converts sqlachemy model into pydantic model
        orm_mode = True

class PostResponse(PostBase): # Define a Pydantic model for the response when getting a post
    id : int
    created_at: datetime
    user_id: int 
    owner: UserResponse
    class config: #it converts sqlachemy model into pydantic model
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr #validates email
    password: str
    username: str
    




class UserLogin(BaseModel):
    email: EmailStr
    password: str



class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None





