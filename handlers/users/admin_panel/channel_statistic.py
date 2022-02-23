from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.callback_data import statistic_months_cd
from loader import dp, db
from states import states


@dp.callback_query_handler(text="channel_statistic")
async def get_channel_statistics(call: CallbackQuery):
    await call.message.edit_text("За какой год показать статистику?")

    await states.Year.year.set()


@dp.message_handler(state=states.Year.year)
async def set_year(message: types.Message, state: FSMContext):
    year = message.text
    try:
        datetime.strptime(year, '%Y')
    except:
        await message.answer("Не правильный формат даты! Формат: гггг")
        return

    yearsMarkup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Декабрь", callback_data=statistic_months_cd.new(month="12",
                                                                                        year=year)),
             InlineKeyboardButton(text="Январь", callback_data=statistic_months_cd.new(month="01",
                                                                                       year=year)),
             InlineKeyboardButton(text="Февраль", callback_data=statistic_months_cd.new(month="02",
                                                                                        year=year))],
            [InlineKeyboardButton(text="Март", callback_data=statistic_months_cd.new(month="03",
                                                                                     year=year)),
             InlineKeyboardButton(text="Апрель", callback_data=statistic_months_cd.new(month="04",
                                                                                       year=year)),
             InlineKeyboardButton(text="Май", callback_data=statistic_months_cd.new(month="05",
                                                                                    year=year))],
            [InlineKeyboardButton(text="Июнь", callback_data=statistic_months_cd.new(month="06",
                                                                                     year=year)),
             InlineKeyboardButton(text="Июль", callback_data=statistic_months_cd.new(month="07",
                                                                                     year=year)),
             InlineKeyboardButton(text="Август", callback_data=statistic_months_cd.new(month="08",
                                                                                       year=year))],
            [InlineKeyboardButton(text="Сентябрь", callback_data=statistic_months_cd.new(month="09",
                                                                                         year=year)),
             InlineKeyboardButton(text="Октябрь", callback_data=statistic_months_cd.new(month="10",
                                                                                        year=year)),
             InlineKeyboardButton(text="Ноябрь", callback_data=statistic_months_cd.new(month="11",
                                                                                       year=year))],
            [InlineKeyboardButton(text="Весь год", callback_data=statistic_months_cd.new(month="0",
                                                                                         year=year))]
        ]
    )

    await message.answer("За какой месяц показать статистику?", reply_markup=yearsMarkup)

    await state.finish()


@dp.callback_query_handler(statistic_months_cd.filter(month="0"))
async def get_statistic_year(call: CallbackQuery, callback_data: dict):
    year = callback_data["year"]

    request1 = f"to_char(registration_date,'yyyy') = '{year}'"
    request2 = f"to_char(recovery_date,'yyyy') = '{year}'"
    request3 = f"to_char(deleteauto_date,'yyyy') = '{year}'"
    request4 = f"to_char(ban_date,'yyyy') = '{year}'"
    request5 = f"to_char(cancel_date,'yyyy') = '{year}'"

    new_users = await db.get_count_users(request1)
    recovery_users = await db.get_count_users(request2)
    delete_no_pay = await db.get_count_users(request3)
    banned_users = await db.get_count_users(request4)
    cancel_sub_users = await db.get_count_users(request5)

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("Выбрать другой год и месяц", callback_data="channel_statistic")]
        ]
    )

    await call.message.edit_text(text=f"Новые пользователи - {new_users}\n"
                                      f"Вернувшиеся пользователи - {recovery_users}\n\n"
                                      f"Удалены за неуплату - {delete_no_pay}\n"
                                      f"Попали в БАН - {banned_users}\n"
                                      f"Отменили подписку - {cancel_sub_users}",
                                 reply_markup=markup)


@dp.callback_query_handler(statistic_months_cd.filter())
async def get_statistic_months(call: CallbackQuery, callback_data: dict):
    month = callback_data["month"]
    year = callback_data["year"]

    request1 = f"to_char(registration_date,'yyyy-mm') = '{year}-{month}'"
    request2 = f"to_char(recovery_date,'yyyy-mm') = '{year}-{month}'"
    request3 = f"to_char(deleteauto_date,'yyyy-mm') = '{year}-{month}'"
    request4 = f"to_char(ban_date,'yyyy-mm') = '{year}-{month}'"
    request5 = f"to_char(cancel_date,'yyyy-mm') = '{year}-{month}'"

    new_users = await db.get_count_users(request1)
    recovery_users = await db.get_count_users(request2)
    delete_no_pay = await db.get_count_users(request3)
    banned_users = await db.get_count_users(request4)
    cancel_sub_users = await db.get_count_users(request5)

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("Выбрать другой год и месяц", callback_data="channel_statistic")]
        ]
    )

    await call.message.edit_text(text=f"Новые пользователи - {new_users}\n"
                                      f"Вернувшиеся пользователи - {recovery_users}\n\n"
                                      f"Удалены за неуплату - {delete_no_pay}\n"
                                      f"Попали в БАН - {banned_users}\n"
                                      f"Отменили подписку - {cancel_sub_users}",
                                 reply_markup=markup)
