from datetime import datetime

from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from loader import dp, db


@dp.callback_query_handler(text="overdue_users")
async def get_overdue_users(call: CallbackQuery):
    await call.message.delete()

    users = await db.get_overdue_users()

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("Инструкция по дальнейшим действиям", callback_data="instruction_for_action")]
        ]
    )

    temp = 0

    for user in users:
        if user[1]:
            if datetime.now().date() > user[1]:
                temp += 1
                await call.message.answer(f"Внимание! Найден пользователь с просроченной пропиской: @{user[0]}\n"
                                          f"Подписка до: {user[1]}, последняя оплата: {user[2]}", reply_markup=markup)
    if temp == 0:
        await call.message.answer("Пользователи с просроченными подписками не найдены")


@dp.callback_query_handler(text="instruction_for_action")
async def get_instruction(call: CallbackQuery):
    await call.message.edit_text("""Необходимо сверить дату последней оплаты в этом чате. 
Для этого необходимо ввести в строке поиска username пользователя и просмотреть все сообщения
о подтверждении оплаты этого пользователя.\n
Если дата последней оплаты подтвердится, то это значит работа моих алгоритмов дала сбой и этому пользователю
не было отправлено сообщение о продлении подписки. Для решения этой проблемы сообщи эту инфу тех. специалисту. 
А так же будет нужно решить вопрос с оплатой подписки с пользователем.\n
Если есть дата оплаты в чате позже, чем дата оплаты, которую отправил я, 
значит мои алгоритмы дали сбой. Сообщи эту инфу тех. специалисту. В таком случае пользователя беспокоить не нужно.
""")
