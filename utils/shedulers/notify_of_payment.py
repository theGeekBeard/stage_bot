import asyncio

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import bot, _, db


async def notify_of_payment(user_id):
    await asyncio.sleep(3600)

    if await db.get_user_status(user_id) == 0:

        return await bot.send_message(chat_id=user_id, text="Вы не завершили оформление подписки на канал.\nПосле "
                                                            "совершения перевода, отправьте сюда скриншот банковской "
                                                            "операции. \nВ ответ вы получите ссылку на телеграм-канал.")
    else:
        return
