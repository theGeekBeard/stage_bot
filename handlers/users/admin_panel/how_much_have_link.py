import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from loader import dp, db, _
from states import states


@dp.callback_query_handler(text="how_much_have_link")
async def ask_date(call: CallbackQuery):
    users = await db.get_users_with_status(7)

    await call.message.edit_text(_("Введите дату ОТ в формате дд.мм.гггг"),
                                 reply_markup=None)

    await states.Date.first_date.set()


@dp.message_handler(state=states.Date.first_date)
async def get_calculations(message: types.Message, state: FSMContext):
    date = message.text
    try:
        datetime.datetime.strptime(date, '%d.%m.%Y')
    except:
        await message.answer(_("Не правильный формат даты! Формат: дд.мм.гггг"))
        return

    date_dt = datetime.datetime.strptime(date, '%d.%m.%Y')
    date_st = datetime.datetime.strftime(date_dt, '%Y-%m-%d')

    async with state.proxy() as data:
        data["date1"] = date_st

    await message.answer(_("Введите дату ДО в формате дд.мм.гггг"))

    await states.Date.second_date.set()


@dp.message_handler(state=states.Date.second_date)
async def get_calculations(message: types.Message, state: FSMContext):
    date = message.text
    try:
        datetime.datetime.strptime(date, '%d.%m.%Y')
    except:
        await message.answer(_("Не правильный формат даты! Формат: дд.мм.гггг"))
        return

    date_dt = datetime.datetime.strptime(date, '%d.%m.%Y')
    date_st = datetime.datetime.strftime(date_dt, '%Y-%m-%d')

    async with state.proxy() as data:
        date1 = data["date1"]

    count_user = await db.get_count_user_with_link(date1, date_st)

    await message.answer(_("{count} получили ссылку").format(count=count_user[0]))

    await state.finish()
