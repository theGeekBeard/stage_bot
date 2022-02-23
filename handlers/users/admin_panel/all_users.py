from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from loader import dp, db


@dp.callback_query_handler(text="all_users")
async def get_all_users(call: CallbackQuery):
    request1 = "status = 1 OR status = 2 OR status = 3 OR status = 4 OR status = 5 OR status = 6 OR status = 11"
    request2 = "status = 3"
    request3 = "status = 7"
    request4 = "status = 9"
    request5 = "status = 8"

    total_amount = await db.get_count_users(request1)
    users_with_sub_term = await db.get_count_users(request2)
    delete_users_for_no_pay = await db.get_count_users(request3)
    canceled_sub = await db.get_count_users(request4)
    banned_users = await db.get_count_users(request5)

    await call.message.edit_text(text=f"На канале пользователей - {total_amount}\n"
                                      f"Истекает срок подписки - {users_with_sub_term}\n"
                                      f"Удалено за неуплату подписки - {delete_users_for_no_pay}\n"
                                      f"Самостоятельно отменили подписку - {canceled_sub}\n"
                                      f"В БАНе - {banned_users}", reply_markup=None)
