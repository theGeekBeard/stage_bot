from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from loader import dp, db
from states import states


@dp.callback_query_handler(text="add_operator")
async def add_operator(call: CallbackQuery):
    await call.message.edit_text("Внимание! Оператор должен быть зарегистрован в боте как обычный пользователь\n"
                                 "Введите username нового оператора")

    await states.Operator.username.set()


@dp.message_handler(state=states.Operator.username)
async def set_new_genre(message: types.Message, state: FSMContext):
    username = message.text

    async with state.proxy() as data:
        data['username'] = username

    await message.answer("Теперь введите его user_id (id пользователя в телеграм)\n"
                         "Чтобы узнать user_id пользователя, воспользуйтесь ботом @getmyid_bot."
                         "Пользователь пишет ему любое сообщение, а в ответ он скинет user_id.")

    await states.Operator.user_id.set()


@dp.callback_query_handler(state=states.Operator.user_id)
async def set_new_operator(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        username = data['username']

    user_id = message.text

    await db.add_operator(username, user_id)
    await db.add_user_parameters(user_id, request="status=14")

    await message.answer("Оператор добавлен\nЧтобы у него открылась панель администратора ему необходимо нажать команду"
                         "/start")

    await state.finish()
