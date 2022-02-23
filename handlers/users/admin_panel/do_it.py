from aiogram.types import CallbackQuery

from loader import dp, db


@dp.callback_query_handler(text="do_it")
async def do_it(call: CallbackQuery):
    request1 = "status = 1"
    request2 = "status = 4"
    request3 = "status = 6"
    request4 = "status = 11"
    request5 = "status = 7"

    reg_amount = await db.get_count_users(request1)
    sub_amount = await db.get_count_users(request2)
    change_sub_amount = await db.get_count_users(request3)
    rec_amount = await db.get_count_users(request4)
    non_sub = await db.get_count_users(request5)

    await call.message.edit_text(
        f"Оплата при регистрации - {reg_amount}\n"
        f"Оплата при продлении подписки - {sub_amount}\n"
        f"Оплата при смене тарифа - {change_sub_amount}\n"
        f"Оплата при восстановлении подписки - {rec_amount}\n"
        f"Не продление подписки (удалить) - {non_sub}", reply_markup=None
    )