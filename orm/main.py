from fastapi import FastAPI,Response,status,HTTPException, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine) 

app = FastAPI()


def get_db():
    db = Session_local()
    try:
        yield db
    finally:
        db.close()    


@app.get("/get-posts")
def read_root(db: Session = Depends(get_db)):
    return {"status": "ok", }

