from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from keyboards.inline.callback_data import regions_cd, search_song_cd, genres_cd, level_cd
from loader import dp, _, db
from states import states


@dp.callback_query_handler(text="search_songs")
async def search_song(call: CallbackQuery):
    status = await db.get_user_status(call.message.chat.id)

    if status in (0, 7, 9, 10, 12, 13):
        await call.message.edit_text(
            _("Для того, что бы воспользоваться этой функцией - оформите подписку на телеграм-канал 'Пой со мной'"),
            reply_markup=None)
    elif status == 8:
        await call.message.edit_text(
            _("К сожалению, вы больше не можете пользоваться функциями бота."), reply_markup=None)
    else:
        # markup = InlineKeyboardMarkup(
        #     inline_keyboard=[
        #         # [InlineKeyboardButton(text=_("По названию"), callback_data="on_name")],
        #         [InlineKeyboardButton(text=_("По региону, жанру и(или) уровню сложности"), callback_data="on_other")],
        #         [InlineKeyboardButton(text=_("Вернуться в меню"), callback_data="menu")]
        #     ]
        # )

        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=_("По региону"), callback_data=search_song_cd.new(call="0", value="",
                                                                                             criteria="1"))],
                [InlineKeyboardButton(text=_("По жанру"), callback_data=search_song_cd.new(call="0", value="",
                                                                                           criteria="2"))],
                [InlineKeyboardButton(text=_("По уровню сложности"),
                                      callback_data=search_song_cd.new(call="0", value="",
                                                                       criteria="3"))]
            ]
        )

        await call.message.edit_text(_("По какому критерию будем искать песни?"), reply_markup=markup)


@dp.callback_query_handler(text="on_name")
async def ask_song_name(call: CallbackQuery):
    await call.message.edit_text(_("Введите название песни(обязательно с заглавной буквы)"), reply_markup=None)

    await states.SearchSong.name.set()


@dp.message_handler(state=states.SearchSong.name)
async def search_song_on_name(message: types.Message, state: FSMContext):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=_("Ввести название песни"), callback_data="on_name")],
            [InlineKeyboardButton(text=_("Вернуться в меню поиска"), callback_data="search_songs")]
        ]
    )

    song_name = message.text
    if not song_name[0].istitle():
        await state.finish()

        return await message.answer(_("Некорректное название песни(обязательно с заглавной буквы)"),
                                    reply_markup=markup)

    found_songs = await db.get_song(title=song_name)

    temp = 0
    if found_songs:
        notes = {
            True: "есть",
            False: "нет"
        }
        level = {
            1: _("низкий"),
            2: _("средний"),
            3: _("высокий")
        }
        for song in found_songs:
            temp += 1
            text = f"_____________________\n" \
                   f"{song[0]}, {song[1]}, {song[2]}, {song[3]}, {song[4]}, ноты - {notes[song[5]]}, " \
                   f"ур. сложности - {level[song[6]]}\nПерейти к песне: {song[7]}"
            await message.answer(text)
        await message.answer(_("↓Выберите действие↓"), reply_markup=markup)
    if temp == 0:
        await message.answer(_("Песня с таким названием не найдена\n"
                               "Неправильно введено название или мы еще не добавили эту песню"), reply_markup=markup)

    await state.finish()


@dp.callback_query_handler(text="on_other")
async def ask_criterion(call: CallbackQuery):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=_("По региону"), callback_data=search_song_cd.new(call="0", value="",
                                                                                         criteria="1"))],
            [InlineKeyboardButton(text=_("По жанру"), callback_data=search_song_cd.new(call="0", value="",
                                                                                       criteria="2"))],
            [InlineKeyboardButton(text=_("По уровню сложности"),
                                  callback_data=search_song_cd.new(call="0", value="",
                                                                   criteria="3"))],
            [InlineKeyboardButton(text=_("Вернуться в меню поиска"),
                                  callback_data="search_songs")]
        ]
    )

    await call.message.edit_text(_("Выберите критерий поиска песни"), reply_markup=markup)


@dp.callback_query_handler(search_song_cd.filter(criteria="1"))
async def search_on_region(call: CallbackQuery, callback_data: dict, state: FSMContext):
    regions = await db.get_regions()

    if callback_data['call'] == "2":
        return await search_song_(call, request=callback_data['value'], state=state)

    async with state.proxy() as data:
        data['call'] = callback_data['call']
        data['value'] = callback_data['value']

    markup = InlineKeyboardMarkup()

    for region in regions:
        markup.row(
            InlineKeyboardButton(text=region[1], callback_data=regions_cd.new(id=str(region[0]), name=region[1])))

    await call.message.edit_text(_("Выберите один из регионов для поиска:"), reply_markup=markup)


@dp.callback_query_handler(regions_cd.filter())
async def set_region(call: CallbackQuery, callback_data: dict, state: FSMContext):
    region_id = callback_data["id"]

    async with state.proxy() as data:
        call_status = data['call']
        value = data['value']

    if call_status == "1":
        request = value + f"AND region_id='{region_id}'"

        await search_song_(call, request, state)
    else:
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=_("Начать поиск"),
                                      callback_data=search_song_cd.new(call="2", value=f"region_id='{region_id}'",
                                                                       criteria="1"))],
                [InlineKeyboardButton(text=_("По жанру"),
                                      callback_data=search_song_cd.new(call="1", value=f"region_id='{region_id}'",
                                                                       criteria="2"))],
                [InlineKeyboardButton(text=_("По уровню сложности"),
                                      callback_data=search_song_cd.new(call="1", value=f"region_id='{region_id}'",
                                                                       criteria="3"))]
            ]
        )

        await call.message.edit_text(_("Добавьте еще критерии или начните поиск"), reply_markup=markup)


@dp.callback_query_handler(search_song_cd.filter(criteria="2"))
async def search_on_genre(call: CallbackQuery, callback_data: dict, state: FSMContext):
    genres = await db.get_genres()

    if callback_data['call'] == "2":
        return await search_song_(call, request=f"genre_id={callback_data['value']}", state=state)

    async with state.proxy() as data:
        data['call'] = callback_data['call']
        data['value'] = callback_data['value']

    markup = InlineKeyboardMarkup()

    for genre in genres:
        markup.row(
            InlineKeyboardButton(text=genre[1], callback_data=genres_cd.new(id=str(genre[0]), name=genre[1])))

    await call.message.edit_text(_("Выберите один из жанров для поиска:"), reply_markup=markup)


@dp.callback_query_handler(genres_cd.filter())
async def set_genre(call: CallbackQuery, callback_data: dict, state: FSMContext):
    genre_id = callback_data["id"]

    async with state.proxy() as data:
        call_status = data['call']
        value = data['value']

    if call_status == "1":
        request = value + f"AND genre_id='{genre_id}'"

        await search_song_(call, request, state)
    else:
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=_("Начать поиск"),
                                      callback_data=search_song_cd.new(call="2", value=f"genre_id='{genre_id}'",
                                                                       criteria="1"))],
                [InlineKeyboardButton(text=_("Добавить критерий по региону"),
                                      callback_data=search_song_cd.new(call="1", value=f"genre_id='{genre_id}'",
                                                                       criteria="1"))],
                [InlineKeyboardButton(text=_("Добавить критерий по уровню сложности"),
                                      callback_data=search_song_cd.new(call="1", value=f"genre_id='{genre_id}'",
                                                                       criteria="3"))]
            ]
        )

        await call.message.edit_text(_("Добавьте еще критерии или начните поиск"), reply_markup=markup)


@dp.callback_query_handler(search_song_cd.filter(criteria="3"))
async def search_on_level(call: CallbackQuery, callback_data: dict, state: FSMContext):
    try:
        if callback_data['call'] == "2":
            return await search_song_(call, request=f"level={callback_data['value']}", state=state)
    except:
        pass

    async with state.proxy() as data:
        data['call'] = callback_data['call']
        data['value'] = callback_data['value']

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(_("Низкий"), callback_data=level_cd.new(num="1"))],
            [InlineKeyboardButton(_("Средний"), callback_data=level_cd.new(num="2"))],
            [InlineKeyboardButton(_("Высокий"), callback_data=level_cd.new(num="3"))]
        ]
    )

    await call.message.edit_text(_("Выберите один из уровней сложности для поиска:"), reply_markup=markup)


@dp.callback_query_handler(level_cd.filter())
async def set_level(call: CallbackQuery, state: FSMContext, callback_data: dict):
    level = callback_data["num"]

    async with state.proxy() as data:
        call_status = data['call']
        value = data['value']

    if call_status == "1":
        request = value + f"AND level={level}"
        await search_song_(call, request, state)
    else:
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=_("Начать поиск"),
                                      callback_data=search_song_cd.new(call="2", value=f"level={level}",
                                                                       criteria="1"))],
                [InlineKeyboardButton(text=_("По региону"),
                                      callback_data=search_song_cd.new(call="1", value=f"level={level}",
                                                                       criteria="1"))],
                [InlineKeyboardButton(text=_("По жанру"),
                                      callback_data=search_song_cd.new(call="1", value=f"level={level}",
                                                                       criteria="2"))]
            ]
        )

        await call.message.edit_text(_("Добавьте еще критерии или начините поиск"), reply_markup=markup)


async def search_song_(call: CallbackQuery, request, state: FSMContext):
    found_songs = await db.get_song(request=request)

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=_("Вернуться в меню поиска"), callback_data="search_songs")]
        ]
    )

    if found_songs:
        notes = {
            True: _("есть"),
            False: _("нет")
        }
        level = {
            1: _("низкий"),
            2: _("средний"),
            3: _("высокий")
        }
        await call.message.edit_reply_markup()
        await call.message.answer(_("↓Результаты поиска↓"))
        for song in found_songs:
            text = f"_____________________\n" \
                   f"{song[0]}, {song[1]}, {song[2]}, {song[3]}, {song[4]}, ноты - {notes[song[5]]}, " \
                   f"ур. сложности - {level[song[6]]}\nПерейти к песне: {song[7]}"
            await call.message.answer(text, reply_markup=None)
        await call.message.answer(_("↓Выберите действие↓"), reply_markup=markup)
        await state.finish()
    else:
        await call.message.edit_text(_("Песня с выбранными критериями не найдена"), reply_markup=markup)
        await state.finish()
