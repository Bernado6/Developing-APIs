from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    Title:str
    Content:str
    Published: bool = True
    Rating: Optional[int] = None


my_posts =[{'Title': 'Top ten Technologies to learn in 2024', 'Content': 'Look at this tech that will change your life in 2024', 'Published': True, 'Rating': None, "id": 1}, {'Title': 'Top ten artist in 2024', 'Content': 'Look at this best music in 2024', 'Published': True, 'Rating': None, "id": 2}]


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

@app.get("/")
async def root():
    return {"Message": "Welcome to my APIs!==================="}

# Http Get Method: It gets all the content or multiples objects
@app.get("/posts")
async def get_posts():
    return {"data": my_posts}


# @app.post("/createpost")
# async def create_post(payload: dict = Body(...)):
#     print(payload)
#     return {"new_post": f"title: {payload['Title']} Content: {payload['Content']}"}

# Http POST Method: creating a post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    
    # print(f"Title: {new_post.Title}")
    # print(f"content: {new_post.Content}")
    # print(f"Publish: {new_post.Published}")
    # print(f"Rating: {new_post.Rating}")
    
    post_dict = post.dict()
    post_dict['id']=randrange(0,1000000)
    my_posts.append(post_dict)
    
    
    return {"data" : post_dict}

@app.get("/posts/latest")
def get_latest():
    post = my_posts[len(my_posts)-1]
    return {"Latest Post": post }


# Http Get Method: Getting just one post
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with the id Number: {id} was not found")
    #    response.status_code = status.HTTP_404_NOT_FOUND
    #    return {f"Post with the id Number {id} was not found"}
    print(type(id))
    print(post)
    return {"post_detail": post}