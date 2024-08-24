from fastapi import FastAPI, HTTPException, Response, status, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randint
import psycopg2 
from psycopg2 import Error,OperationalError
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()



@app.get("/") # Root endpoint called decorated with FastAPI
async def root():
    return {"message": "Welcome to FastAPI!"}


class Post(BaseModel): # Define a Pydantic model for the POST data so it can be validated 
    title: str
    content: str
    category: int = 1  # Default value is 1 for unpublished posts and unentered data
    published: bool
    rating: Optional[float] = None

while True:
  try:
      conn = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="Tubelight1@",  cursor_factory=RealDictCursor)
      cursor = conn.cursor()
      print("Database connection established successfully")
      break
  
  except Exception as error:
      print("Connection to database failed")
      print("Error:", error)
      time.sleep(5)  # Wait for 5 seconds before retrying the connection



my_post = [{"title": "My First Post", "content": "This is my first post content","published": 0,"id": 1,"rating": 8.9}, {"title": "My Second Post", "content": "This is my second post content", "id": 2}]



@app.get("/posts") # Endpoint with a parameter called post_id
def get_posts():
    cursor.execute("""SELECT * FROM post""")
    post = cursor.fetchall()
    print(post)
    return {"data": post }


@app.post("/posts") # Endpoint with a parameter called post_id
def create_post(post: Post):
    cursor.execute("""INSERT INTO post (title, content, category, published, rating) VALUES (%s, %s, %s, %s, %s) RETURNING * """, (post.title, post.content, post.category, post.published, post.rating))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/posts/{post_id}") # Endpoint with a parameter called post_id
def get_post(post_id: int, response: Response):
    cursor.execute("""SELECT * FROM post WHERE id = %s""", (post_id,))
    test_post = cursor.fetchone()
    
    if test_post:
        return {"data": test_post}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
#In Python, when you pass a single value as a parameter to a SQL query, it must be in the form of a tuple. A tuple with a single element requires a trailing comma (e.g., (post_id,)). Without the comma, Python would not recognize it as a tuple, which can cause the SQL query to fail or behave unexpectedly.

@app.delete("/posts/{post_id}") # Endpoint with a parameter called post_id
def delete_post(post_id: int, response: Response):
    cursor.execute("""DELETE FROM post WHERE id = %s RETURNING *""", (post_id,))
    delete_post = cursor.fetchone()
    conn.commit()
    if delete_post == None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post WITH id:{post_id} not exixts")
    return {"data": delete_post}


#update post
@app.post("/posts/{post_id}") # Endpoint with a parameter called post_id
def update_post(post_id: int, updated_post: Post, response: Response):
    cursor.execute("""UPDATE post SET title=%s, content=%s, category=%s, published=%s, rating=%s WHERE id=%s RETURNING *""", (updated_post.title, updated_post.content, updated_post.category, updated_post.published, updated_post.rating, post_id))
    updated_post_data = cursor.fetchone()
    conn.commit()
    if updated_post_data == None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post WITH id:{post_id} not exists")
    return {"data": updated_post_data}





