from fastapi import FastAPI, HTTPException, Response, status, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
import time
from . import models, schema,utils
from sqlalchemy.orm import Session
from .database import engine
from .database import get_db
from . routers import user, post,auth




models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user.router) # Include user router in the FastAPI app
app.include_router(post.router)
app.include_router(auth.router) # Include auth router in the FastAPI app


@app.get("/") # Root endpoint called decorated with FastAPI
async def root():
    return {"message": "Welcome to FastAPI!"}































