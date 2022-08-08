from config import models
from fastapi import Depends, FastAPI, HTTPException, status
from config.dbconfig import engine
from sqlalchemy.orm import Session
from src import routes

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get('/')
def home():
    return {"home": "Hello"}


app.include_router(routes.school_router)
app.include_router(routes.class_router)
