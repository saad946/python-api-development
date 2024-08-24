from fastapi import FastAPI, HTTPException, Response, status
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randint


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



my_post = [{"title": "My First Post", "content": "This is my first post content","published": 0,"id": 1,"rating": 8.9}, {"title": "My Second Post", "content": "This is my second post content", "id": 2}]

@app.get("/posts") # Endpoint with a parameter called post_id
def get_posts():
    return {"data": my_post }


@app.post("/posts") # Endpoint with a parameter called post_id
def create_post(post: Post):
    post_dict = post.dict() 
    post_dict["id"] = randint(1, 10000000)  # Assign a random ID for new posts
    my_post.append(post_dict)
    return {"message": post_dict}


@app.get("/posts/{post_id}") # Endpoint with a parameter called post_id
def get_post(post_id: int, response: Response):
    for post in my_post:
        if post["id"] == post_id:
            return {"message": post}
        # else:
        #     response.status_code = status.HTTP_404_NOT_FOUND
        #     return {"message": "Post not found"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

@app.delete("/posts/{post_id}") # Endpoint with a parameter called post_id
def delete_post(post_id: int, response: Response):
    for post in my_post:
        if post["id"] == post_id:
            my_post.remove(post)
            return {"message": "Post succesfully deleted"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post WITH id:{post_id} not found")

#update post
@app.post("/posts/{post_id}") # Endpoint with a parameter called post_id
def update_post(post_id: int, updated_post: Post, response: Response):
    for post in my_post:
        if post["id"] == post_id:
            post.update(updated_post.dict(exclude_unset=True))  # Update only the fields provided in the updated_post Pydantic model
            return {"message": "Post succesfully updated"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post WITH id:{post_id} not found")








@app.post("/createpost") # Endpoint for creating a new post
def create_post(new_post: Post):
    print(f"Received new post: {new_post}")
    print(new_post.title)
    new_post.dict()  # Convert Pydantic model to dict for JSON apiv1.0 compliant apis
    print
    print(new_post.dict())  # Exclude fields with None

    return {"data": new_post}





# @app.post("/createpost") # Endpoint for creating a new post
# def create_post(payload: dict = Body(...)):
#     print(f"Received payload: {payload}")
#     return {"new_post": f"title: {payload['title']}. Content: {payload['content']}"}







# title str, content str, category str, bool published bool




