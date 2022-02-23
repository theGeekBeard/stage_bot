from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from loader import db
from loader import dp
from states import states


@dp.callback_query_handler(text="change_link")
async def change_card(call: CallbackQuery):
    await call.message.edit_text("Введите новую ссылку")

    await states.Link.link.set()

@dp.message_handler(state=states.Link.link)
async def set_new_card_number(message: types.Message, state: FSMContext):
    link = message.text

    await db.set_channel_link(link)

    await message.answer("Ссылка изменена")

    await state.finish()
