from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from loader import dp, db, bot
from states import states


@dp.callback_query_handler(text="ban_user")
async def ban_user(call: CallbackQuery):
    await call.message.edit_text("Введите Username TG пользователя, которого нужно заБАНить (без @)")

    await states.BanUser.username.set()


@dp.message_handler(state=states.BanUser.username)
async def set_username(message: types.Message, state: FSMContext):
    username = message.text

    user_data = await db.get_user_with_data(row_name="username", data=username)

    if user_data:

        async with state.proxy() as data:
            data['username'] = username
            data['name'] = user_data[5]
            data['user_id'] = user_data[-1]

        await message.answer("Укажи причину БАНа (эта информация не будет отправлена пользователю, а только "
                             "сохранится в базе данных)")
        await states.BanUser.reason.set()
    else:
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton("Ввести Username TG еще раз", callback_data="ban_user")]
            ]
        )

        await message.answer("Пользователь с таким Username TG не найден", reply_markup=markup)
        await state.finish()


@dp.message_handler(state=states.BanUser.reason)
async def set_reason_ban(message: types.Message, state: FSMContext):
    reason = message.text

    async with state.proxy() as data:
        username = data['username']
        user_id = data['user_id']
        name = data['name']

    request = f"status = 8, subscription_date = null, rate_id = null, recovery_date = null, " \
              f"ban_date = '{datetime.now().date()}', reason_delete = '{reason}'"

    await db.add_user_parameters(user_id, request=request)

    await bot.send_message(user_id, f"Привет, {name}. Вы были удалены из телеграм-канала 'Пой со "
                                    f"мной' за нарушение правил. К сожалению, у Вас нет возможности вернуться в канал.")

    await message.answer(f"Пользователь @{username} отправлен в БАН!")

    await state.finish()

