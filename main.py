import asyncio
from aiogram import Bot, Dispatcher

from handlers import user_commands, start_generate, upload_file, force_check

from data.database import initialize_db
from config import TOKEN, DB_PATH


async def main():
    await initialize_db(DB_PATH)

    bot = Bot(TOKEN)
    dp = Dispatcher()

    dp.include_routers(
        user_commands.router,
        start_generate.router,
        upload_file.router,
        force_check.router,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
