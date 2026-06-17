import asyncio
from asyncio import CancelledError

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from app.config import BOT
from app.db.connector import async_engine
from app.models import Base
from app.handlers.general import router as welcome_router
from app.handlers.notes import router as notes_router


async def create_db_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def start_bot(bot: Bot):
    dp = Dispatcher()
    dp.include_router(welcome_router)
    dp.include_router(notes_router)

    await bot.set_my_commands([
        BotCommand(command="/start", description="Начало"),
        BotCommand(command="/help", description="Помощь"),
    ])

    print("Starting bot...")
    try:
        await dp.start_polling(bot)
    except CancelledError:
        pass
    finally:
        print("Bot stopped")


async def main():
    await create_db_tables()
    await start_bot(BOT)


if __name__ == '__main__':
    asyncio.run(main())
