from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_data import delete_sug_song_cd
from loader import dp, db


@dp.callback_query_handler(text="suggest_songs")
async def get_suggest_songs(call: CallbackQuery, state: FSMContext):
    await call.message.delete()

    suggest_songs = await db.get_suggest_song()
    for song in suggest_songs:
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton("Удалить песню", callback_data=delete_sug_song_cd.new(id=song[0]))]
            ]
        )
        await call.message.answer(f"{song[0]}: {song[1]}: @{song[2]}", reply_markup=markup)
    else:
        await call.message.answer("Нет предложенных песен на данный момент")


@dp.callback_query_handler(delete_sug_song_cd.filter())
async def delete_sug_song(call: CallbackQuery, callback_data: dict):
    song_id = callback_data["id"]

    await db.delete_sug_song(song_id)

    await call.message.edit_text("Песня удалена из предложенных")
