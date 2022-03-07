from aiogram.types import CallbackQuery

from loader import dp, db


@dp.callback_query_handler(text="users_tariffs")
async def get_user_tariffs(call: CallbackQuery):
    request1 = "rate_id = 1 AND status != 0 AND status != 13 AND status != 8 AND status != 12 AND status != 10"
    request2 = "rate_id = 2 AND status != 0 AND status != 13 AND status != 8 AND status != 12 AND status != 10"
    request3 = "rate_id = 3 AND status != 0 AND status != 13 AND status != 8 AND status != 12 AND status != 10"

    month1 = await db.get_count_users(request1)
    month2 = await db.get_count_users(request2)
    month3 = await db.get_count_users(request3)

    await call.message.edit_text(text=f"1 месяц - {month1}\n"
                                      f"6 месяцев - {month2}\n"
                                      f"12 месяцев - {month3}")
