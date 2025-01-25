from fastapi import FastAPI, Response, status, HTTPException 
from pydantic import BaseModel 
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True


while True:
    try:
        conn = psycopg2.connect(host="localhost",database="fastapi",user="postgres",password="abuzar",cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connected successfully")
        break
    except Exception as error:
        print("Database connection failed", error)
        print("Error:" , error)
        time.sleep(2)


    

my_posts = [{
    "title": "My first post",
    "content": "This is the content of my first post.",
    "id": 1
}]


def get_post_id(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i
    # return -1            

@app.post("/create-post", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict();
    post_dict['id'] = randrange(0,1000000)
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    new_post=cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()
    if not post:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    return {"data": post}


# delete post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response):
    
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not exist")


#update_post

@app.put("/post/{id}")
def update_post(id: int, post: Post):
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s  RETURNING * """, (post.title, post.content, post.published))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    return {"data": updated_post}    
