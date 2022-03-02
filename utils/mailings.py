from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_data import confirm_payment_cd
from loader import db, bot


async def notify_operator(user_id, username, payment_type=0, notify_type=0):
    operators = await db.get_all_admins()

    userInfo = await db.get_user(user_id)
    rate = await db.get_rates_info(user_id)

    name = userInfo[6]
    surname = userInfo[7]
    inst = userInfo[8]
    city = userInfo[11]
    registrationDate = userInfo[13]
    paymentScreenshot = userInfo[-1]

    text = f"Tg: @{username}\n" \
           f"Имя: {name}\n" \
           f"Фамилия: {surname}\n" \
           f"Instagram: {inst}\n" \
           f"Город: {city}\n" \
           f"Тариф подписки: {rate[0]}₽\n" \
           f"Дата регистрации: {registrationDate}\n\n"

    if payment_type == 1:
        btnText = "Подтвердить оплату при продлении подписки"
    elif payment_type == 2:
        btnText = "Подтвердить оплату при смене тарифа"
    elif payment_type == 3:
        btnText = "Подтвердить оплату при восстановлении подписки"
    else:
        btnText = "Подтвердить оплату при регистрации"

    confirmPaymentBtn = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=btnText, callback_data=confirm_payment_cd.new(
                username=username, user_id=user_id
            ))]
        ]
    )

    if notify_type == 2:
        caption = "Пользователь сменил тариф подписки!\n\n"
    elif notify_type == 1:
        caption = "Пользователь продлил подписку!\n\n"
    elif notify_type == 3:
        caption = "Пользователь восстановил подписку!\n\n"
    else:
        caption = "Зарегистрирован новый пользователь\n\n"

    for operator in operators:
        try:
            await bot.send_photo(operator[0], photo=paymentScreenshot, caption=caption + text,
                                 reply_markup=confirmPaymentBtn)
        except:
            await bot.send_document(operator[0], document=paymentScreenshot, caption=caption + text,
                                    reply_markup=confirmPaymentBtn)


async def notify_operator_about_delete_user(user_id, username, notify_type=0):
    operators = await db.get_all_admins()

    userInfo = await db.get_user(user_id)

    name = userInfo[6]
    surname = userInfo[7]
    inst = userInfo[8]

    text = f"Tg: @{username}\n" \
           f"Имя: {name}\n" \
           f"Фамилия: {surname}\n" \
           f"Instagram: {inst}\n"

    if notify_type == 1:
        caption = "К сожалению, пользователь принял решение отменить подписку\n\n"
    else:
        caption = "У пользователя закончилась подписка. Его нужно удалить из канала!\n\n"

    for operator in operators:
        await bot.send_message(operator[0], text=caption + text)


async def notify_operator_about_reason(username, reason):
    operators = await db.get_all_admins()

    for operator in operators:
        await bot.send_message(operator[0], f"Пользователь @{username} указал причину отмены подписки:"
                                            f"{reason}")
