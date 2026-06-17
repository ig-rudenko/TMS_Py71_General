import os

from aiogram import Bot
from dotenv import load_dotenv
load_dotenv()

DB_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///db.sqlite3")

BOT = Bot(token=os.getenv("BOT_TOKEN", ""))
