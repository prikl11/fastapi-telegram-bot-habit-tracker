from sqlalchemy.orm import Session
from schemas import HabitCreate, HabitUpdate
from models import Habits

def create_habit(db: Session, habit: HabitCreate):
    new_habit = Habits()