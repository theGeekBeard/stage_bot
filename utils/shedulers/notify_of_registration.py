import asyncio

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import bot, _, db


async def notify_of_registration(user_id):
    await asyncio.sleep(3600)

    if await db.get_user_status(user_id) == 13:
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(_('Регистрация'), callback_data="registration_user")]
            ]
        )

        return await bot.send_message(chat_id=user_id, text="Вы не завершили регистрацию. Если у вас возникли трудности с "
                                                      "регистрацией - напишите нам, мы поможем @QA_support",
                                reply_markup=markup)
    else:
        return
