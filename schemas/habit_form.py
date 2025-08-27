from aiogram.filters.state import State, StatesGroup

class HabitForm(StatesGroup):
    title = State()
    frequency = State()
    times_per_day = State()
    remind_at = State()