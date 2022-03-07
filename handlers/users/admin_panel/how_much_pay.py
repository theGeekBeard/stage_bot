import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from loader import dp, db, _
from states import states


@dp.callback_query_handler(text="how_much_pay")
async def ask_date(call: CallbackQuery):
    users = await db.get_users_with_status(7)

    await call.message.edit_text(_("Введите дату ОТ в формате дд.мм.гггг"),
                                 reply_markup=None)

    await states.Date.date.set()


@dp.message_handler(state=states.Date.date)
async def ask_date2(message: types.Message, state: FSMContext):
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

    await states.Date.date2.set()


@dp.message_handler(state=states.Date.date2)
async def get_calculations(message: types.Message, state: FSMContext):
    date = message.text
    try:
        datetime.datetime.strptime(date, '%d.%m.%Y')
    except:
        await message.answer(_("Не правильный формат даты! Формат: дд.мм.гггг"))
        return

    async with state.proxy() as data:
        date2 = data["date1"]

    date_dt = datetime.datetime.strptime(date, '%d.%m.%Y')
    date_st = datetime.datetime.strftime(date_dt, '%Y-%m-%d')

    payment_calculations = await db.get_payment_amount(date2, date_st)

    if payment_calculations[1]:
        await message.answer(_("Кол-во оплат: {payment_count}\n"
                               "Общая сумма: {payment_amount}").format(payment_count=payment_calculations[0],
                                                                       payment_amount=payment_calculations[1]))
    else:
        await message.answer(_("В эти дни оплат проведено не было"))

    await state.finish()
