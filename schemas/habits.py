from datetime import datetime
from pydantic import BaseModel
from schemas import Frequency


class HabitCreate(BaseModel):
    title: str
    frequency: Frequency
    times_per_day: int
    remind_at: datetime

class HabitUpdate(BaseModel):
    title: str | None = None
    times_per_day: int | None = None
    is_active: bool | None = None

class HabitOut(BaseModel):
    id: int
    title: str
    frequency: Frequency
    times_per_day: int
    remind_at: datetime
    streak: int
    longest_streak: int
    created_at: datetime
    is_active: bool