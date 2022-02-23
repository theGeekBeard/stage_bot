from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from loader import dp, _, db


@dp.callback_query_handler(text="ask_question")
async def ask_question(call: CallbackQuery):
    status = await db.get_user_status(call.message.chat.id)

    if status in (9, 12):
        await call.message.edit_text(
            _("Для того, что бы воспользоваться этой функцией - оформите подписку на телеграм-канал 'Пой со мной'"),
            reply_markup=None)
    elif status == 8:
        await call.message.edit_text(
            _("К сожалению, вы больше не можете пользоваться функциями бота."), reply_markup=None)
    else:
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(_("Вернуться в меню"), callback_data="menu")]
        ])

        await call.message.edit_text(_("На ваши вопросы ответит Лизавета. Вот ее телеграм @lisaveta_support"),
                                     reply_markup=markup)
