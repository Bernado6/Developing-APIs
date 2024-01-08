from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time 
app = FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published: bool = True
    # Rating: Optional[int] = None
    
while True:    
    try:
        conn = psycopg2.connect(host='localhost', 
                                database= 'fastapi',
                                port=5433,
                                user='postgres',
                                password='postgres', 
                                cursor_factory= RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as e:
        print("Failed to connect to database")
        print("Error:", e)
        time.sleep(3)


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
    cursor.execute(""" SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"data":posts}


# @app.post("/createpost")
# async def create_post(payload: dict = Body(...)):
#     print(payload)
#     return {"new_post": f"title: {payload['Title']} Content: {payload['Content']}"}

# Http POST Method: creating a post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                   (post.title, post.content, post.published)) # We are using named tuple from
    new_post = cursor.fetchone()
    conn.commit()

    return {"data" : new_post}

@app.get("/posts/latest")
def get_latest():
    post = my_posts[len(my_posts)-1]
    return {"Latest Post": post }


# Http Get Method: Getting just one post
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    post = cursor.fetchone()
    # post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with the id Number: {id} was not found")
    #    response.status_code = status.HTTP_404_NOT_FOUND
    #    return {f"Post with the id Number {id} was not found"}
    # print(type(id))
    print(post)
    return {"post_detail": post}

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i
        
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id), ))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            ,detail=f"The  post with the id {id} does not exist")
        
    return {"msg":"Post with the id {id} has been deleted successfully!"}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            ,detail=f"The  post with the id {id} does not exist")

    return {"msg": "Post Updated successfully!", "data": updated_post}
    
    
    