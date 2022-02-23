from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from loader import db
from loader import dp
from states import states


@dp.callback_query_handler(text="add_genre")
async def add_genre(call: CallbackQuery):
    genres = await db.get_genres()

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("Отмена", callback_data="cancel_adding")]
        ]
    )

    await call.message.delete()

    for genre in genres:
        await call.message.answer(genre[1])

    await call.message.answer("Введите название жанра для добавления, если его нет в списке", reply_markup=markup)

    await states.RegionGenre.genre.set()


@dp.message_handler(state=states.RegionGenre.genre)
async def set_new_genre(message: types.Message, state: FSMContext):
    genre = message.text

    await db.add_genre(genre)

    await message.answer("Жанр добавлен")

    await state.finish()