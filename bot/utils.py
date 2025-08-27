from aiogram import Bot, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from models import Users, Habits
import os
from dotenv import load_dotenv
import asyncio
from crud import read_habits, create_habit
from contextlib import contextmanager
from database import SessionLocal
from schemas import HabitForm

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@dp.message(F.text == "/start")
async def start_command(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username

    with get_db() as db:
        user = db.query(Users).filter(Users.telegram_id == user_id).first()
        if not user:
            user = Users(telegram_id=user_id, username=username)
            db.add(user)
            db.commit()
            db.refresh(user)

    await message.reply(f"Привет, {username}!")

@dp.message(F.text == "/habits")
async def read_habits_command(message: Message):
    user_id = message.from_user.id

    with get_db() as db:
        habits = read_habits(db, user_id)
        if not habits:
            await message.reply("Вы не добавляли привычек")
            return

        habits_text = "\n".join([f"- {habit.title}\nЧастота напоминания: {habit.frequency}\nКоличество в день: {habit.times_per_day}\nПродолжительность серии: {habit.streak}\nСамая долгая серия: {habit.longest_streak}\nСтатус: {habit.is_active}" for habit in habits])
        await message.reply(f"Ваши привычки:\n{habits_text}")

@dp.message(F.text == "/create")
async def create_habit_command(message: Message, state: FSMContext):
    await message.answer("Как называется привычка?")
    await state.set_state(HabitForm.title)

@dp.message()
async def get_title(message: Message, state: FSMContext):
    user_id = message.from_user.id

    with get_db() as db:
        current_state = await state.get_state()

        if current_state == HabitForm.title:
            await state.update_data(title=message.text)
            await message.answer("Как часто? (daily, weekly, monthly, custom)")
            await state.set_state(HabitForm.frequency)

        elif current_state == HabitForm.frequency:
            await state.update_data(frequency=message.text)
            await message.answer("Сколько раз в день?")
            await state.set_state(HabitForm.times_per_day)

        elif current_state == HabitForm.times_per_day:
            await state.update_data(times_per_day=message.text)
            await message.answer("Во сколько напоминать?")
            await state.set_state(HabitForm.remind_at)

        elif current_state == HabitForm.remind_at:
            await state.update_data(remind_at=message.text)
            data = await state.get_data()

            create_habit(db, data, user_id)
            await message.answer(
                f"Привычка создана:\n"
                f"Название: {data['title']}\n"
                f"Частота: {data['frequency']}\n"
                f"Раз в день: {data['times_per_day']}\n"
                f"Напоминание: {data['remind_at']}\n"
            )
            await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())