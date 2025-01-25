from fastapi import FastAPI,Response,status,HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    

# Connect to PostgreSQL database

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



@app.get("/")
def get():
    return {"message": "Hello, World!"}   


# create a new post

@app.post("/create-post", status_code= status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"message": "Post created successfully", "data": new_post}


# get all posts

@app.get("/posts", )
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"message": "All posts", "data": posts}

# get post by id

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    post = cursor.fetchone()
    if not post:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    return {"data": post}


# updated post 

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """ UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
        (post.title, post.content, post.published, id)
    )
    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return {"data": updated_post}


# Delete a post

@app.delete("/posts/{id}")
def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s """, (str(id),))
    post_delete = cursor.fetchone()
    conn.commit()
    if post_delete == None:
        

    return {"message": "Post deleted successfully"}
    


