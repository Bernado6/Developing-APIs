from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    Title:str
    Content:str
    Published: bool = True
    Rating: Optional[int] = None


my_posts =[{'Title': 'Top ten Technologies to learn in 2024', 'Content': 'Look at this tech that will change your life in 2024', 'Published': True, 'Rating': None}, {'Title': 'Top ten artist in 2024', 'Content': 'Look at this best music in 2024', 'Published': True, 'Rating': None}]

@app.get("/")
async def root():
    return {"Message": "Welcome to my APIs!==================="}

@app.get("/posts")
async def get_posts():
    return {"data": my_posts}


# @app.post("/createpost")
# async def create_post(payload: dict = Body(...)):
#     print(payload)
#     return {"new_post": f"title: {payload['Title']} Content: {payload['Content']}"}
@app.post("/posts")
async def create_post(new_post: Post):
    
    # print(f"Title: {new_post.Title}")
    # print(f"content: {new_post.Content}")
    # print(f"Publish: {new_post.Published}")
    # print(f"Rating: {new_post.Rating}")
    print(new_post)
    print(new_post.dict())
    
    return {"data" :"new_post"}