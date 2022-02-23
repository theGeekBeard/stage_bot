from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from keyboards.inline.callback_data import change_price_cd
from loader import db
from loader import dp
from states import states


@dp.callback_query_handler(text="change_price")
async def change_tariff_price(call: CallbackQuery):
    rates = await db.get_rates()

    markup = InlineKeyboardMarkup()

    for rate in rates:
        markup.row(
            InlineKeyboardButton(text=f"{rate[1]} ({rate[2]}р.)",
                                 callback_data=change_price_cd.new(rate_id=rate[0])))

    await call.message.edit_text("Цену какого тарифа нужно изменить?", reply_markup=markup)


@dp.callback_query_handler(change_price_cd.filter())
async def ask_new_price(call: CallbackQuery, callback_data: dict, state: FSMContext):
    async with state.proxy() as data:
        data['rate_id'] = callback_data['rate_id']

    await call.message.answer("Введи новую цену тарифа")

    await states.NewPrice.price.set()


@dp.message_handler(state=states.NewPrice.price)
async def set_new_price(message: types.Message, state: FSMContext):
    try:
        price = int(message.text)
    except:
        return await message.answer("Неправильный формат цены")

    async with state.proxy() as data:
        rate_id = data['rate_id']

    await db.update_rate_price(rate_id, price)

    await message.answer("Цена тарифа изменена")

    await state.finish()
