from aiogram import types
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from loader import dp, _, db, bot
from states import states


@dp.callback_query_handler(text="suggest_song")
async def suggest_song(call: CallbackQuery):
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

        await call.message.edit_text(
            _("Если в канале нет песни, которая вам нужна, то вы можете предложить нам эту песню и мы постараемся "
              "добавить ее в канал.\nВведите одним сообщением название песни, село и регион, и отправьте ее мне\nИли "
              "нажмите 'Вернуться в меню' для отмены этого действия"), reply_markup=markup)

        await states.SuggestSong.info.set()


@dp.message_handler(state=states.SuggestSong.info)
async def set_song_data(message: types.Message):
    await bot.edit_message_reply_markup(message.chat.id, message.message_id - 1)

    song_info = message.text

    await db.add_suggest_song(song_info, message.chat.username, True)

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(_("Вернуться в меню"), callback_data="menu")]
    ])

    await message.answer(_("Спасибо! Я передам песню администратору канала."), reply_markup=markup)
