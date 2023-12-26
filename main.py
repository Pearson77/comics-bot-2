import asyncio
import config

from aiogram import Bot, Dispatcher
from handlers import router


async def main():
    bot = Bot(token=config.TOKEN)
    dp = Dispatcher(bot=bot)

    dp.include_router(router=router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
