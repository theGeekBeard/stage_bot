from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from loader import dp


@dp.message_handler(text="Действия", state="*")
async def get_admin_menu(message: types.Message, state: FSMContext):
    print(2)
    await state.finish()

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("Пользователи", callback_data="users_main")],
            [InlineKeyboardButton("Статистика", callback_data="statistic_main")],
            [InlineKeyboardButton("Песни", callback_data="song_main")],
            [InlineKeyboardButton("Изменение данных", callback_data="data_main")],
        ]
    )

    await message.answer("Ваше меню:", reply_markup=markup)


@dp.callback_query_handler(text="statistic_main")
async def get_statistic_menu(call: CallbackQuery):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("Пользователи", callback_data="all_users")],
            [InlineKeyboardButton("Тарифы пользователей", callback_data="users_tariffs")],
            [InlineKeyboardButton("Статистика канала", callback_data="channel_statistic")]
        ])

    await call.message.edit_text(f"Время сервера: {datetime.now()}", reply_markup=markup)


@dp.callback_query_handler(text="song_main")
async def song_menu(call: CallbackQuery):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("Добавить песню", callback_data="add_song")],
            [InlineKeyboardButton("Изменить песню", callback_data="change_song")],
            [InlineKeyboardButton("Предложенные песни", callback_data="suggest_songs")],
            [InlineKeyboardButton("Добавить регион", callback_data="add_region")],
            [InlineKeyboardButton("Добавить жанр", callback_data="add_genre")]
        ])

    await call.message.edit_text(f"Время сервера: {datetime.now()}", reply_markup=markup)


@dp.callback_query_handler(text="data_main")
async def get_data(call: CallbackQuery):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("Изменить номер карты", callback_data="change_card")],
            [InlineKeyboardButton("Изменить цену тарифа", callback_data="change_price")],
            [InlineKeyboardButton("Изменить ссылку на канал", callback_data="change_link")]
        ])

    await call.message.edit_text(f"Время сервера: {datetime.now()}", reply_markup=markup)


@dp.callback_query_handler(text="users_main")
async def get_users_menu(call: CallbackQuery):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("Нужно сделать", callback_data="do_it")],
            [InlineKeyboardButton("Подтверждение оплаты", callback_data="confirm_payment")],
            [InlineKeyboardButton("Не продленные подписки", callback_data="non_subscription_users")],
            [InlineKeyboardButton("Сомневающиеся пользователи", callback_data="doubters_users")],
            [InlineKeyboardButton("Изменить статус пользователя", callback_data="change_status")],
            [InlineKeyboardButton("Поиск пользователя", callback_data="search_user")],
            [InlineKeyboardButton("ЗаБАНить пользователя", callback_data="ban_user")],
            [InlineKeyboardButton("Просроченные подписки", callback_data="overdue_users")],
            [InlineKeyboardButton("Поиск лишних пользователей на канале", callback_data="search_non_users")],
            [InlineKeyboardButton("Добавить оператора", callback_data="add_operator")]
        ])

    await call.message.edit_text(f"Время сервера: {datetime.now()}", reply_markup=markup)
