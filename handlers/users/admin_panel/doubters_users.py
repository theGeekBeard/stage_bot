from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from loader import dp, db


@dp.callback_query_handler(text="doubters_users")
async def get_doubters_users(call: CallbackQuery):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("Начали регистрацию, но не завершили", callback_data="reg")],
            [InlineKeyboardButton("Зарегистрировались, но не оплатили", callback_data="reg_no_pay")],
            [InlineKeyboardButton("Сменили тариф, но не оплатили", callback_data="tariff_no_pay")],
            [InlineKeyboardButton("Хотят восстановиться, но не оплатили", callback_data="rec_no_pay")]
        ]
    )

    await call.message.edit_text("Выберите", reply_markup=markup)


@dp.callback_query_handler(text="reg")
async def get_doubters_users_start_registration(call: CallbackQuery):
    users = await db.get_users_with_status(13)

    if users:
        user_list = []
        for user in users:
            user_list.append(f"<code>@{user[0]}</code>")
        await call.message.edit_text(text=",".join(user_list), parse_mode="HTML")
    else:
        await call.message.edit_text("Пользователей не нашлось")


@dp.callback_query_handler(text="reg_no_pay")
async def get_doubters_users_start_registration_no_pay(call: CallbackQuery):
    users = await db.get_users_with_status(0)

    if users:
        user_list = []
        for user in users:
            user_list.append(f"<code>@{user[0]}</code>")
        await call.message.edit_text(text=",".join(user_list), parse_mode="HTML")
    else:
        await call.message.edit_text("Пользователей не нашлось")


@dp.callback_query_handler(text="tariff_no_pay")
async def get_doubters_users_changed_tariff_no_pay(call: CallbackQuery):
    users = await db.get_users_with_status(5)

    if users:
        user_list = []
        for user in users:
            user_list.append(f"<code>@{user[0]}</code>")
        await call.message.edit_text(text=",".join(user_list), parse_mode="HTML")
    else:
        await call.message.edit_text("Пользователей не нашлось")


@dp.callback_query_handler(text="rec_no_pay")
async def get_doubters_users_recovery_no_pay(call: CallbackQuery):
    users = await db.get_users_with_status(10)

    if users:
        user_list = []
        for user in users:
            user_list.append(f"<code>@{user[0]}</code>")
        await call.message.edit_text(text=",".join(user_list), parse_mode="HTML")
    else:
        await call.message.edit_text("Пользователей не нашлось")