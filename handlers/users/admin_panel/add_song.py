from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from keyboards.inline.callback_data import add_song_cd, notes_cd, level_cd, adding_song_cd
from loader import db, bot
from loader import dp
from states import states


@dp.callback_query_handler(text="add_song")
async def ask_name(call: Union[CallbackQuery, types.Message], state: FSMContext, callback_data: dict = False,
                   isChange=False):
    async with state.proxy() as data:
        data['isChange'] = isChange

    if isinstance(call, CallbackQuery):
        await call.message.edit_text("Название песни", reply_markup=None)
    else:
        await bot.delete_message(call.chat.id, call.message_id - 1)
        await call.answer("Название песни")

    await states.Song.name.set()


@dp.message_handler(state=states.Song.name)
async def ask_village(message: types.Message, state: FSMContext, callback_data: dict = False, isChange=False):
    name = message.text

    async with state.proxy() as data:
        if name != "Что нужно изменить?":
            data['name'] = name
        status = data['isChange']
        data['isChange'] = isChange

    if status:
        return await confirm_adding_song(message, state)

    await message.answer("Село (с приставкой в начале - “с.”, “д.” или “п.”)")
    await states.Song.village.set()


@dp.message_handler(state=states.Song.village)
async def ask_district(message: types.Message, state: FSMContext, callback_data: dict = False, isChange=False):
    village = message.text

    async with state.proxy() as data:
        if village != "Что нужно изменить?":
            data['village'] = village
        status = data['isChange']
        data['isChange'] = isChange

    if status:
        return await confirm_adding_song(message, state)

    await message.answer("Район (с приставкой район или р-н)")
    await states.Song.district.set()


@dp.message_handler(state=states.Song.district)
async def ask_region(message: types.Message, state: FSMContext, callback_data: dict = False, isChange=False):
    district = message.text

    async with state.proxy() as data:
        if district != "Что нужно изменить?":
            data['district'] = district
        status = data['isChange']
        data['isChange'] = isChange

    if status:
        return await confirm_adding_song(message, state)

    regions = await db.get_regions()

    markup = InlineKeyboardMarkup()

    for region in regions:
        markup.row(
            InlineKeyboardButton(text=region[1], callback_data=add_song_cd.new(region_id=str(region[0]),
                                                                               region_name=region[1],
                                                                               genre_id="0", genre_name="0")))

    await message.answer("Выбери регион из списка", reply_markup=markup)
    await states.Song.region.set()


@dp.callback_query_handler(add_song_cd.filter(genre_name="0"), state=states.Song.region)
async def ask_genre(call: CallbackQuery, state: FSMContext, callback_data: dict = False, isChange=False):
    try:
        region_id = callback_data["region_id"]
        region_name = callback_data["region_name"]
        async with state.proxy() as data:
            data['region_id'] = region_id
            data['region_name'] = region_name
    except:
        pass

    async with state.proxy() as data:
        status = data['isChange']
        data['isChange'] = isChange

    if status:
        await call.message.delete()
        return await confirm_adding_song(call.message, state)

    genres = await db.get_genres()

    markup = InlineKeyboardMarkup()

    for genre in genres:
        markup.row(
            InlineKeyboardButton(text=genre[1], callback_data=add_song_cd.new(region_id="0",
                                                                              region_name="0",
                                                                              genre_id=str(genre[0]),
                                                                              genre_name=genre[1])))

    if isinstance(call, CallbackQuery):
        await call.message.edit_reply_markup()
        await call.message.answer("Выбери жанр из списка", reply_markup=markup)
    elif isinstance(call, types.Message):
        message = call
        await message.answer("Выбери жанр из списка", reply_markup=markup)

    await states.Song.genre.set()


@dp.callback_query_handler(add_song_cd.filter(region_name="0"), state=states.Song.genre)
async def ask_notes(call: CallbackQuery, state: FSMContext, callback_data: dict = False, isChange=False):
    try:
        genre_id = callback_data["genre_id"]
        genre_name = callback_data["genre_name"]
        async with state.proxy() as data:
            data['genre_id'] = genre_id
            data['genre_name'] = genre_name
    except:
        pass

    async with state.proxy() as data:
        status = data['isChange']
        data['isChange'] = isChange

    if status:
        await call.message.delete()
        return await confirm_adding_song(call.message, state)

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("Да", callback_data=notes_cd.new(value="True"))],
            [InlineKeyboardButton("Нет", callback_data=notes_cd.new(value="False"))]
        ]
    )

    if isinstance(call, CallbackQuery):
        await call.message.edit_reply_markup()
        await call.message.answer("Есть ли ноты к песне?", reply_markup=markup)
    elif isinstance(call, types.Message):
        message = call
        await message.answer("Есть ли ноты к песне?", reply_markup=markup)

    await states.Song.notes.set()


@dp.callback_query_handler(notes_cd.filter(), state=states.Song.notes)
async def ask_level(call: CallbackQuery, state: FSMContext, callback_data: dict = False, isChange=False):
    try:
        notes = callback_data["value"]
        async with state.proxy() as data:
            data['notes'] = notes
    except:
        pass

    async with state.proxy() as data:
        status = data['isChange']
        data['isChange'] = isChange

    if status:
        await call.message.delete()
        return await confirm_adding_song(call.message, state)

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("Низкий(1)", callback_data=level_cd.new(num="1"))],
            [InlineKeyboardButton("Средний(2)", callback_data=level_cd.new(num="2"))],
            [InlineKeyboardButton("Высокий(3)", callback_data=level_cd.new(num="3"))]
        ]
    )

    if isinstance(call, CallbackQuery):
        await call.message.edit_reply_markup()
        await call.message.answer("Какой уровень сложности?", reply_markup=markup)
    elif isinstance(call, types.Message):
        message = call
        await message.answer("Какой уровень сложности?", reply_markup=markup)

    await states.Song.level.set()


@dp.callback_query_handler(level_cd.filter(), state=states.Song.level)
async def ask_telegram_id(call: CallbackQuery, state: FSMContext, callback_data: dict = False, isChange=False):
    try:
        level = callback_data["num"]
        async with state.proxy() as data:
            data['level'] = level
    except:
        pass

    async with state.proxy() as data:
        status = data['isChange']
        data['isChange'] = isChange

    if status:
        await call.message.delete()
        return await confirm_adding_song(call.message, state)

    if isinstance(call, CallbackQuery):
        await call.message.edit_reply_markup()
        await call.message.answer("Номер песни в ТГ канале “Пой со мной”")
    elif isinstance(call, types.Message):
        message = call
        await message.answer("Номер песни в ТГ канале “Пой со мной”")

    await states.Song.telegram_id.set()


@dp.message_handler(state=states.Song.telegram_id)
async def ask_link(message: types.Message, state: FSMContext, callback_data: dict = False, isChange=False):
    telegram_id = message.text

    async with state.proxy() as data:
        if telegram_id != "Что нужно изменить?":
            try:
                int(telegram_id)
                if await db.get_song_with_id(telegram_id):
                    return await message.answer("Песня с таким номером уже есть! Введите другой номер")
            except:
                return await message.answer("Неправильный номер")
            data['telegram_id'] = telegram_id
        status = data['isChange']
        data['isChange'] = isChange

    if status:
        return await confirm_adding_song(message, state)

    await message.answer("Укажи ссылку на песню в ТГ-канале “Пой со мной”")
    await states.Song.link.set()


@dp.message_handler(state=states.Song.link)
async def set_link(message: types.Message, state: FSMContext, callback_data: dict = False):
    link = message.text

    async with state.proxy() as data:
        data['link'] = link

    await confirm_adding_song(message, state)


async def confirm_adding_song(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        name = data["name"]
        village = data["village"]
        district = data["district"]
        region_id = data["region_id"]
        region_name = data["region_name"]
        genre_id = data["genre_id"]
        genre_name = data["genre_name"]
        notes = data["notes"]
        level = data['level']
        telegram_id = data['telegram_id']
        link = data['link']
        data['isChange'] = False

    text = f"""Название: {name}
Село: {village}
Район: {district}
Регион: {region_name}
Жанр: {genre_name}
Есть ли ноты: {notes}
Уровень сложности: {level}
Номер песни в канале: {telegram_id}
Ссылка: {link}
Проверь ссылку еще, что бы убедиться, что она верная!\n
Все верно?"""

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Да",
                                  callback_data="yes_add"),
             InlineKeyboardButton(text="Нет",
                                  callback_data="no_change")],
            [InlineKeyboardButton(text="Отменить", callback_data="cancel_adding")]
        ]
    )

    await message.answer(text, reply_markup=markup)
    await state.reset_state(with_data=False)


@dp.callback_query_handler(text="cancel_adding", state="*")
async def cancel_adding(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Действие отменено", reply_markup=None)
    await state.finish()


@dp.callback_query_handler(text="yes_add")
async def add_songs(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        name = data["name"]
        village = data["village"]
        district = data["district"]
        region_id = data["region_id"]
        genre_id = data["genre_id"]
        notes = data["notes"]
        level = data['level']
        telegram_id = data['telegram_id']
        link = data['link']

    rows_names = "telegram_id, title, village, district, region_id, genre_id, notes, level, link, activity"
    values = f"{telegram_id}, '{name}', '{village}', '{district}', {region_id}, {genre_id}, {notes}, {level}, '{link}', True "

    await db.add_song(rows_names, values)

    await call.message.edit_text("Песня успешно добавлена", reply_markup=None)


@dp.callback_query_handler(text="no_change")
async def get_change_parameters(call: CallbackQuery):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Название", callback_data=adding_song_cd.new(number="1"))],
            [InlineKeyboardButton(text="Село", callback_data=adding_song_cd.new(number="2"))],
            [InlineKeyboardButton(text="Район", callback_data=adding_song_cd.new(number="3"))],
            [InlineKeyboardButton(text="Регион", callback_data=adding_song_cd.new(number="4"))],
            [InlineKeyboardButton(text="Жанр", callback_data=adding_song_cd.new(number="5"))],
            [InlineKeyboardButton(text="Есть ли ноты", callback_data=adding_song_cd.new(number="6"))],
            [InlineKeyboardButton(text="Уровень сложности", callback_data=adding_song_cd.new(number="7"))],
            [InlineKeyboardButton(text="Номер песни", callback_data=adding_song_cd.new(number="8"))],
            [InlineKeyboardButton(text="Ссылка", callback_data=adding_song_cd.new(number="9"))],
        ]
    )

    await call.message.edit_text("Что нужно изменить?", reply_markup=markup)


@dp.callback_query_handler(adding_song_cd.filter())
async def change_registration_value(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.delete()

    number = callback_data.get("number")

    levels = {
        "1": ask_name,
        "2": ask_village,
        "3": ask_district,
        "4": ask_region,
        "5": ask_genre,
        "6": ask_notes,
        "7": ask_level,
        "8": ask_telegram_id,
        "9": ask_link
    }

    navigation_function = levels[number]

    await navigation_function(call.message, callback_data=callback_data, state=state, isChange=True)
