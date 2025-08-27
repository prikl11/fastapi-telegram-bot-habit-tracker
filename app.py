from typing import Annotated
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db, Base, engine
from crud import read_users, create_habit, read_habits, update_habit, delete_habit
from schemas import HabitOut, HabitUpdate, HabitCreate, UserOut

app = FastAPI()

Base.metadata.create_all(bind=engine)
SessionDep = Annotated[Session, Depends(get_db)]

@app.get("/home")
def home():
    return {"message": "Welcome to this app!"}

@app.get("/users", response_model=list[UserOut])
def read_users_route(db: SessionDep):
    return read_users(db)

@app.get("/habits", response_model=list[HabitOut])
def read_habits_route(db: SessionDep, user_id: int):
    return read_habits(db, user_id)

@app.post("/habits", response_model=HabitOut)
def create_habit_route(db: SessionDep, habit: HabitCreate, user_id: int):
    return create_habit(db, habit, user_id)

@app.patch("/habits/{habit_id}", response_model=HabitOut)
def update_habit_route(db: SessionDep, habit_id: int, habit: HabitUpdate, user_id: int):
    return update_habit(db, habit_id, habit, user_id)

@app.delete("/habits/{habit_id}", response_model=HabitOut)
def delete_habit_route(db: SessionDep, habit_id: int, user_id: int):
    return delete_habit(db, habit_id, user_id)