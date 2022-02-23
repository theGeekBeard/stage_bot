from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from loader import dp, db


@dp.callback_query_handler(text="confirm_payment")
async def confirm_payment(call: CallbackQuery):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("Оплата при регистрации", callback_data="pay_registration")],
            [InlineKeyboardButton("Оплата при продлении подписки", callback_data="pay_subscription")],
            [InlineKeyboardButton("Оплата при смене тарифа", callback_data="pay_tariff")],
            [InlineKeyboardButton("Оплата при восстановлении подписки", callback_data="pay_recovery")]
        ]
    )

    await call.message.edit_text("Выберите:", reply_markup=markup)


@dp.callback_query_handler(text="pay_registration")
async def get_pay_registration(call: CallbackQuery):
    users = await db.get_users_with_status(1)

    if users:
        user_list = []
        for user in users:
            user_list.append(f"<code>@{user[0]}</code>")
        await call.message.edit_text(text=",".join(user_list), parse_mode="HTML")
    else:
        await call.message.edit_text("Пользователей не нашлось")


@dp.callback_query_handler(text="pay_subscription")
async def get_pay_subscription(call: CallbackQuery):
    users = await db.get_users_with_status(4)

    if users:
        user_list = []
        for user in users:
            user_list.append(f"<code>@{user[0]}</code>")
        await call.message.edit_text(text=",".join(user_list), parse_mode="HTML")
    else:
        await call.message.edit_text("Пользователей не нашлось")


@dp.callback_query_handler(text="pay_tariff")
async def get_pay_tariff(call: CallbackQuery):
    users = await db.get_users_with_status(6)

    if users:
        user_list = []
        for user in users:
            user_list.append(f"<code>@{user[0]}</code>")
        await call.message.edit_text(text=",".join(user_list), parse_mode="HTML")
    else:
        await call.message.edit_text("Пользователей не нашлось")


@dp.callback_query_handler(text="pay_recovery")
async def get_pay_recovery(call: CallbackQuery):
    users = await db.get_users_with_status(11)

    if users:
        user_list = []
        for user in users:
            user_list.append(f"<code>@{user[0]}</code>")
        await call.message.edit_text(text=",".join(user_list), parse_mode="HTML")
    else:
        await call.message.edit_text("Пользователей не нашлось")
