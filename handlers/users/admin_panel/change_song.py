from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from keyboards.inline.callback_data import change_song_cd, change_song_btns_cd
from loader import dp, db
from states import states


@dp.callback_query_handler(text="change_song")
async def change_song(call: CallbackQuery):
    await call.message.edit_text("Введи номер песни в ТГ канале 'Пой со мной'")

    await states.ChangeSong.telegram_id.set()


@dp.message_handler(state=states.ChangeSong.telegram_id)
async def get_song(message: types.Message, state: FSMContext):
    telegram_id = message.text

    request = f"musics.telegram_id = {telegram_id}"
    song_data = await db.get_song(request=request)
    print(song_data)

    if song_data:
        async with state.proxy() as data:
            data["song_id"] = song_data[0][8]

        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=f"Название - {song_data[0][0]}",
                                      callback_data=change_song_cd.new(row_name='title',
                                                                       type='text'))],
                [InlineKeyboardButton(text=f"Село - {song_data[0][1]}",
                                      callback_data=change_song_cd.new(row_name='village',
                                                                       type='text'))],
                [InlineKeyboardButton(text=f"Район - {song_data[0][2]}",
                                      callback_data=change_song_cd.new(row_name='district',
                                                                       type='text'))],
                [InlineKeyboardButton(text=f"Регион - {song_data[0][3]}",
                                      callback_data=change_song_cd.new(row_name='region_id',
                                                                       type='btn'))],
                [InlineKeyboardButton(text=f"Жанр - {song_data[0][4]}",
                                      callback_data=change_song_cd.new(row_name='genre_id',
                                                                       type='btn'))],
                [InlineKeyboardButton(text=f"Есть ли ноты - {song_data[0][5]}",
                                      callback_data=change_song_cd.new(row_name='notes',
                                                                       type='btn'))],
                [InlineKeyboardButton(text=f"Уровень сложности - {song_data[0][6]}",
                                      callback_data=change_song_cd.new(row_name='level',
                                                                       type='btn'))],
                [InlineKeyboardButton(text=f"Номер песни - {song_data[0][8]}",
                                      callback_data=change_song_cd.new(row_name='telegram_id',
                                                                       type='text'))],
                [InlineKeyboardButton(text=f"Ссылка - {song_data[0][7]}", callback_data=change_song_cd.new(row_name='link',
                                                                                                        type='text'))],
                [InlineKeyboardButton(text=f"Отображение в поиске - {song_data[0][9]}",
                                      callback_data=change_song_cd.new(row_name='activity',
                                                                       type='btn'))]
            ]
        )

        await message.answer("Что нужно изменить?", reply_markup=markup)
    else:
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton("Ввести номер еще раз", callback_data="change_song")]
            ]
        )

        await message.answer("Песня с таким номером не найдена\nПопробуй еще раз", reply_markup=markup)

    await state.reset_state(with_data=False)


@dp.callback_query_handler(change_song_cd.filter(type='text'))
async def change_song_text(call: CallbackQuery, callback_data: dict, state: FSMContext):
    async with state.proxy() as data:
        data["row_name"] = callback_data["row_name"]

    await call.message.edit_text("Введите значение")
    await states.ChangeSong.value.set()


@dp.message_handler(state=states.ChangeSong.value)
async def set_new_value(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        row_name = data["row_name"]
        song_id = data["song_id"]

    try:
        value = int(message.text)
        request = f"{row_name} = {value}"
    except:
        value = message.text
        request = f"{row_name} = '{value}'"

    await db.update_song(request, song_id=song_id)

    await message.answer("Новые данные песни успешно записаны.")

    await state.reset_state(with_data=False)


@dp.callback_query_handler(change_song_cd.filter(type='btn'))
async def change_song_btn(call: CallbackQuery, callback_data: dict, state: FSMContext):
    row_name = callback_data['row_name']

    async with state.proxy() as data:
        data["row_name"] = callback_data["row_name"]

    if row_name == 'region_id':
        regions = await db.get_regions()

        markup = InlineKeyboardMarkup()

        for region in regions:
            markup.row(
                InlineKeyboardButton(text=region[1], callback_data=change_song_btns_cd.new(value=str(region[0]))))

    elif row_name == 'genre_id':
        genres = await db.get_genres()

        markup = InlineKeyboardMarkup()

        for genre in genres:
            markup.row(
                InlineKeyboardButton(text=genre[1], callback_data=change_song_btns_cd.new(value=str(genre[0]))))

    elif row_name == "notes":
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton("Да", callback_data=change_song_btns_cd.new(value="True"))],
                [InlineKeyboardButton("Нет", callback_data=change_song_btns_cd.new(value="False"))]
            ]
        )

    elif row_name == 'level':
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton("Низкий(1)", callback_data=change_song_btns_cd.new(value="1"))],
                [InlineKeyboardButton("Средний(2)", callback_data=change_song_btns_cd.new(value="2"))],
                [InlineKeyboardButton("Высокий(3)", callback_data=change_song_btns_cd.new(value="3"))]
            ]
        )
    else:
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton("Да", callback_data=change_song_btns_cd.new(value="True"))],
                [InlineKeyboardButton("Нет", callback_data=change_song_btns_cd.new(value="False"))]
            ]
        )

    await call.message.edit_text("Выберите значение", reply_markup=markup)


@dp.callback_query_handler(change_song_btns_cd.filter())
async def set_new_value(call: CallbackQuery, callback_data: dict, state: FSMContext):
    async with state.proxy() as data:
        row_name = data["row_name"]
        song_id = data["song_id"]

    value = callback_data["value"]

    request = f"{row_name} = {value}"

    await db.update_song(request, song_id)

    await call.message.edit_text("Новые данные песни успешно записаны.", reply_markup=None)

    await state.finish()
