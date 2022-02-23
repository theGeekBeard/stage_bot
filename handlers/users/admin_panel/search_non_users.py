from aiogram.types import CallbackQuery

from loader import dp, db, bot


@dp.callback_query_handler(text="search_non_users")
async def search_non_users(call: CallbackQuery):
    await call.message.delete()
    request = "status = 0 OR status = 7 OR status = 8 OR status = 9 OR status = 10 OR status = 12 OR status = 13"
    non_users = await db.get_non_users(request)

    temp = 0

    if non_users:
        for non_user in non_users:
            isNonUser = await bot.get_chat_member(-1001614950824, non_user[0])
            if isNonUser:
                temp += 1
                await call.message.answer(f"На канале найден лишний пользователь!\n"
                                          f"Есть в базе, но со статусом неактивных пользователей\n"
                                          f"@{non_user[1]}")
        if temp == 0:
            await call.message.answer("Лишние пользователи на канале не найдены")
    else:
        await call.message.answer("Лишние пользователи на канале не найдены")
