from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, database  # Import models and database

app = FastAPI()

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/create-post")
async def create_post(post, db: Session = Depends(get_db)):
    new_post = models.Post(title=post.title, content=post.content)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"message": "Post created successfully", "post": new_post}

@app.get("/")
async def root():
    return {"message": "Hello, FastAPI!"}
