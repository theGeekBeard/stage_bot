from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from loader import dp, _, db


@dp.callback_query_handler(text="song_decoding")
async def song_decoding(call: CallbackQuery):
    status = await db.get_user_status(call.message.chat.id)

    if status in (0, 7, 9, 10, 12, 13):
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

        await call.message.edit_text(_("По этому вопросу напишите Лизавете. Вот телеграм  @lisaveta_support\n"
                                       "Она сориентирует вас по стоимости и срокам расшифровки"),
                                     reply_markup=markup)

