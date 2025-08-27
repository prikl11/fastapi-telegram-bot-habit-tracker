from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from fastapi import Depends
from sqlalchemy.orm import Session
from models import Users
from database import get_db, SessionLocal
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(F.text == "/start")
async def start_command(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username

    db = SessionLocal()
    try:
        user = db.query(Users).filter(Users.telegram_id == user_id).first()
        if not user:
            user = Users(user_id=user_id, username=username)
            db.add(user)
            db.commit()
            db.refresh(user)
    finally:
        db.close()

    await message.reply(f"Привет, {username}!")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())