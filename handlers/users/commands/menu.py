from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from loader import dp, _, db


@dp.message_handler(commands=["menu"], state="*")
async def show_menu_cmd(message: types.Message, state: FSMContext):
    await state.finish()

    admins = await db.get_admins(message.chat.id)

    if admins:
        markup = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='Действия'),
                 KeyboardButton(text='Меню')]
            ], resize_keyboard=True
        )
        return await message.answer(_("Меню:"), reply_markup=markup)

    user = await db.get_user(message.chat.id)

    if user:
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=_("Поиск песен"), callback_data="search_songs")],
                [InlineKeyboardButton(text=_("Предложить песню"), callback_data="suggest_song")],
                [InlineKeyboardButton(text=_("Хочу расшифровку песни"), callback_data="song_decoding")],
                [InlineKeyboardButton(text=_("Задать вопрос"), callback_data="ask_question")],
                [InlineKeyboardButton(text=_("Хочу подписку"), callback_data="want_subscription")],
                [InlineKeyboardButton(text=_("Что умеет бот?"), callback_data="can_bot")]
            ]
        )

        await message.answer(_("Выберите:"), reply_markup=markup)
    else:
        await message.answer("Зарегистрируйтесь, чтобы использовать эту функцию\n"
                             "Register to use this feature")


@dp.callback_query_handler(text="menu", state="*")
async def show_menu_cd(call: CallbackQuery, state: FSMContext):
    await state.finish()

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=_("Поиск песен"), callback_data="search_songs")],
            [InlineKeyboardButton(text=_("Предложить песню"), callback_data="suggest_song")],
            [InlineKeyboardButton(text=_("Хочу расшифровку песни"), callback_data="song_decoding")],
            [InlineKeyboardButton(text=_("Задать вопрос"), callback_data="ask_question")],
            [InlineKeyboardButton(text=_("Хочу подписку"), callback_data="want_subscription")],
            [InlineKeyboardButton(text=_("Что умеет бот?"), callback_data="can_bot")]
        ]
    )

    await call.message.edit_text(_("Выберите:"), reply_markup=markup)


@dp.message_handler(text=["Меню", "Menu"], state="*")
async def show_menu(message: types.Message, state: FSMContext):
    await state.finish()

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=_("Поиск песен"), callback_data="search_songs")],
            [InlineKeyboardButton(text=_("Предложить песню"), callback_data="suggest_song")],
            [InlineKeyboardButton(text=_("Хочу расшифровку песни"), callback_data="song_decoding")],
            [InlineKeyboardButton(text=_("Задать вопрос"), callback_data="ask_question")],
            [InlineKeyboardButton(text=_("Хочу подписку"), callback_data="want_subscription")],
            [InlineKeyboardButton(text=_("Что умеет бот?"), callback_data="can_bot")]
        ]
    )

    await message.answer(_("↓Выберите действие↓"), reply_markup=markup)
