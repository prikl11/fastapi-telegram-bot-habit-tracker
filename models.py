from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import Column, Integer, Text, String, Enum, DateTime, Boolean, ForeignKey
from schemas import Frequency

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, index=True, unique=True)
    username = Column(String(50), index=True)

    habits = relationship("Habits", back_populates="user")

class Habits(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    title = Column(Text, index=True)
    frequency = Column(Enum(Frequency, name="frequency_enum"), index=True)
    times_per_day = Column(Integer, index=True)
    remind_at = Column(DateTime(timezone=True), index=True)
    streak = Column(Integer, index=True)
    longest_streak = Column(Integer, index=True)
    created_at = Column(DateTime(timezone=True), index=True)
    is_active = Column(Boolean, index=True, default=True)

    user = relationship("Users", back_populates="habits")
    logs = relationship("HabitLogs", back_populates="habit")

class HabitLogs(Base):
    __tablename__ = "habit_logs"

    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey("habits.id"), index=True)
    date = Column(DateTime(timezone=True), index=True)
    status = Column(String, index=True)
    count = Column(Integer, index=True, default=1)

    habit = relationship("Habits", back_populates="logs")