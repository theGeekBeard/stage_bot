from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from loader import db
from loader import dp
from states import states


@dp.callback_query_handler(text="add_region")
async def add_region(call: CallbackQuery):
    await call.message.delete()
    regions = await db.get_regions()

    for region in regions:
        await call.message.answer(region[1])

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("Отмена", callback_data="cancel_adding")]
        ]
    )

    await call.message.answer("Введите название региона для добавления, если его нет в списке", reply_markup=markup)

    await states.RegionGenre.region.set()


@dp.message_handler(state=states.RegionGenre.region)
async def set_new_region(message: types.Message, state: FSMContext):
    region = message.text

    await db.add_region(region)

    await message.answer("Регион добавлен")
    await state.finish()
