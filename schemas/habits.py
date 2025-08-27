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
    streak: int | None = None
    longest_streak: int | None = None
    created_at: datetime | None = None
    is_active: bool