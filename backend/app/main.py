from fastapi import FastAPI
from . import models
from .database import engine

# This line tells SQLAlchemy to create all tables defined in models.py
# if they don't already exist in the database file.
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Usher Management System")

@app.get("/")
def read_root():
    return {"status": "Online", "message": "Usher API is running."}
