from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import dp, db, _


@dp.message_handler()
async def get_registration_form(message: types.Message):
    status = await db.check_user(message.chat.id)
    print(status)
    if status:
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(_('Регистрация'), callback_data="registration_user")]
            ]
        )

        if status[0] in (0, 12, 13):
            await message.answer(_("Вы не завершили регистрацию.\n"
                                   "Если у вас возникли трудности с регистрацией - напишите нам, мы поможем "
                                   "@lisaveta_support"), reply_markup=markup)
        else:
            pass