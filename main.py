import asyncio

from aiogram import executor, types

import middlewares, handlers, filters

from loader import dp, bot
from utils.notify_admins import on_startup_notify
from utils.shedulers.check_subscribe import check_access


async def on_startup(dispatcher):
    asyncio.create_task(check_access())

    # Notifies about launch
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    from middlewares.throttling_middleware import ThrottlingMiddleware

    dp.middleware.setup(ThrottlingMiddleware())
    executor.start_polling(dp, on_startup=on_startup)
