from aiogram.types import CallbackQuery

from loader import dp, db


@dp.callback_query_handler(text="non_subscription_users")
async def get_non_subscription_users(call: CallbackQuery):
    await call.message.delete()
    users = await db.get_users_with_status(7)

    for user in users:
        await call.message.answer(f"Найден пользователь с непродленной подпиской: <code>{user[0]}</code>",
                                  parse_mode="HTML")
    else:
        await call.message.answer(f"Пользователей с непродленной подпиской нет")
