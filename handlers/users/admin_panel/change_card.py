from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from loader import db
from loader import dp
from states import states


@dp.callback_query_handler(text="change_card")
async def change_card(call: CallbackQuery):
    now_card = await db.get_card_number()

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("Да", callback_data="yes_card")]
        ]
    )

    await call.message.edit_text(
        f"Текущий номер карты: {now_card}\n"
        f"Меняем номер карты? (для отмены процедуры не нажимай 'Да')", reply_markup=markup
    )


@dp.callback_query_handler(text="yes_card")
async def ask_new_card_number(call: CallbackQuery):
    await call.message.edit_text("Введите новый номер карты")

    await states.Card.number.set()


@dp.message_handler(state=states.Card.number)
async def set_new_card_number(message: types.Message, state: FSMContext):
    card_number = message.text

    await db.set_card_number(card_number)

    await message.answer("Карта изменена")

    await state.finish()
