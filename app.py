import asyncio

from aiogram import executor
import aioschedule

from loader import dp
import middlewares, filters, handlers
from utils.checker import check_user_exists
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def scheduler():
    aioschedule.every().day.at("00:00").do(check_user_exists)
    # aioschedule.every().second.do(check_user_exists)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
