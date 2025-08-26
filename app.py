from fastapi import FastAPI
from database import get_db, Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/home")
def home():
    return {"message": "Welcome to this app!"}