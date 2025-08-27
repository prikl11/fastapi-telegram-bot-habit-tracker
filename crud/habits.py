from fastapi import HTTPException
from sqlalchemy.orm import Session
from schemas import HabitCreate, HabitUpdate
from models import Habits, Users

def create_habit(db: Session, habit: HabitCreate, user_id: int):
    user = db.query(Users).filter(Users.telegram_id == user_id).first()
    new_habit = Habits(user_id=user.id,
                       title=habit.title,
                       frequency=habit.frequency,
                       times_per_day=habit.times_per_day,
                       remind_at=habit.remind_at)
    db.add(new_habit)
    db.commit()
    db.refresh(new_habit)
    return new_habit

def read_habits(db: Session, user_id: int):
    user = db.query(Users).filter(Users.telegram_id == user_id).first()
    habits = db.query(Habits).filter(Habits.user_id == user.id).all()
    return habits

def update_habit(db: Session, habit_id: int, habit: HabitUpdate, user_id: int):
    user = db.query(Users).filter(Users.telegram_id == user_id).first()
    existing_habit = db.query(Habits).filter(Habits.id == habit_id,
                                             Habits.user_id == user_id).first()
    if not existing_habit:
        raise HTTPException(status_code=404, detail="Habit not found")

    if habit.title is not None:
        existing_habit.title = habit.title
    if habit.times_per_day is not None:
        existing_habit.times_per_day = habit.times_per_day
    if habit.is_active is not None:
        existing_habit.is_active = habit.is_active

    db.commit()
    db.refresh(existing_habit)
    return existing_habit

def delete_habit(db: Session, habit_id: int, user_id: int):
    habit = db.query(Habits).filter(Habits.id == habit_id,
                                    Habits.user_id == user_id).first()
    if habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")

    db.delete(habit)
    db.commit()
    return {"message": "Habit deleted"}