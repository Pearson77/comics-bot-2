import asyncio
import config

from aiogram import Bot, Dispatcher
from handlers import manage_handlers, read_handlers


async def main():
    bot = Bot(token=config.TOKEN)
    dp = Dispatcher(bot=bot)

    dp.include_router(router=manage_handlers.router)
    dp.include_router(router=read_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
