from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.callback_data import change_status_cd
from loader import dp, db
from states import states


@dp.callback_query_handler(text="change_status")
async def change_status(call: CallbackQuery):
    await call.message.edit_text("Введите Username TG пользователя")

    await states.ChangeStatus.username.set()


@dp.message_handler(state=states.ChangeStatus.username)
async def set_username(message: types.Message, state: FSMContext):
    username = message.text

    user_data = await db.get_user_with_data(row_name="username", data=username)

    if user_data:
        async with state.proxy() as data:
            data['user_id'] = user_data[-1]

        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton("0", callback_data=change_status_cd.new(status="0")),
                 InlineKeyboardButton("1", callback_data=change_status_cd.new(status="1")),
                 InlineKeyboardButton("2", callback_data=change_status_cd.new(status="2"))],
                [InlineKeyboardButton("3", callback_data=change_status_cd.new(status="3")),
                 InlineKeyboardButton("4", callback_data=change_status_cd.new(status="4")),
                 InlineKeyboardButton("5", callback_data=change_status_cd.new(status="5"))],
                [InlineKeyboardButton("6", callback_data=change_status_cd.new(status="6")),
                 InlineKeyboardButton("7", callback_data=change_status_cd.new(status="7")),
                 InlineKeyboardButton("8", callback_data=change_status_cd.new(status="8"))],
                [InlineKeyboardButton("9", callback_data=change_status_cd.new(status="9")),
                 InlineKeyboardButton("10", callback_data=change_status_cd.new(status="10")),
                 InlineKeyboardButton("11", callback_data=change_status_cd.new(status="11"))],
                [InlineKeyboardButton("12", callback_data=change_status_cd.new(status="12")),
                 InlineKeyboardButton("13", callback_data=change_status_cd.new(status="13")),
                 InlineKeyboardButton("14", callback_data=change_status_cd.new(status="14"))],

            ]
        )

        await message.answer("""0 - новый пользователь, который только зарегистрировался, но не отправлял скрин оплаты, 
1 - новый пользователь, который зарегистрировался, оплатил подписку и оплату нужно подтвердить, 
2 - текущий пользователь, оплативший подписку,
3 - текущий пользователь, у которого истекает подписка
4 - текущий пользователь, продлил подписку и оплату нужно подтвердить
5 - текущий пользователь сменил тариф, но не оплатил его
6 - текущий пользователь сменил тариф, оплатил подписку и оплату нужно подтвердить
7 - пользователь, которого удалили из за непродления подписки (автоматическое удаление)
8 - БАН пользователь, которого удалил оператор  
9 - пользователь, который сам отменил подписку 
10 - пользователь, который решил восстановить подписку
11 - пользователь восстанавливает подписку и нужно подтвердить оплату
12 - не стал оплачивать (статус для тех, кто запустил процедуру оплаты, его дожимали, но пользователь отказался платить)
13 - пользователь начал регистрацию, но не завершил ее
14 - администратор (не учитывается в статистике)""", reply_markup=markup)

        await state.reset_state(with_data=False)
    else:
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton("Ввести Username TG еще раз", callback_data="change_status")]
            ]
        )

        await message.answer("Пользователь с таким Username TG не найден", reply_markup=markup)
        await state.finish()


@dp.callback_query_handler(change_status_cd.filter())
async def set_status(call: CallbackQuery, callback_data: dict, state: FSMContext):
    status = int(callback_data["status"])

    async with state.proxy() as data:
        user_id = data['user_id']

    await db.update_user_parameters(user_id, "status", status)

    await call.message.edit_text("Статус пользователя изменен.", reply_markup=None)
