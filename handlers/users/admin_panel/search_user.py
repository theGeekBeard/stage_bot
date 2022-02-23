from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from loader import dp, db
from states import states


@dp.callback_query_handler(text="search_user")
async def search_user(call: CallbackQuery):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("Username tg", callback_data="username_search")],
            [InlineKeyboardButton("Instagram-аккаунт", callback_data="instagram_search")]
        ]
    )
    await call.message.edit_text("Как будем искать пользователя?", reply_markup=markup)


@dp.callback_query_handler(text="username_search")
async def search_user_with_username(call: CallbackQuery):
    await call.message.edit_text("Введи Username tg пользователя (без @)")

    await states.Search.username.set()


@dp.message_handler(state=states.Search.username)
async def set_username(message: types.Message, state: FSMContext):
    status_type = {
        0: "новый пользователь, зарегался, но не оплатил",
        1: "новый пользователь, оплатил подписку, оплату нужно подтвердить",
        2: "текущий пользователь, подписка оплачена",
        3: "текущий пользователь, подписка истекает",
        4: "текущий пользователь, продлил подписку, оплату нужно подтвердить",
        5: "текущий пользователь сменил тариф, но не оплатил его",
        6: "текущий пользователь сменил тариф, оплатил подписку, оплату нужно подтвердить",
        7: "автоматически удален за неуплату подписки",
        8: "пользователь в БАНе",
        9: "пользователь, отменивший подписку",
        10: "пользователь восстанавливает подписку, но не оплатил",
        11: "пользователь восстанавливает подписку, нужно подтвердить оплату",
        12: "начал процедуру, но решил не оплачивать",
        13: "начал регистрацию, но не завершил её"
    }

    username = message.text

    user_data = await db.get_user_with_data(row_name="username", data=username)

    if user_data:
        username = user_data[0]
        tariff = user_data[1]
        sub_term = user_data[3]
        payment_date = user_data[4]
        name = user_data[5]
        surname = user_data[6]
        instagram = user_data[7]
        birthday = user_data[8]
        city = user_data[9]
        status = status_type[user_data[10]]
        registration_date = user_data[11]
        deleteauto_date = user_data[12]
        cancel_date = user_data[13]
        ban_date = user_data[14]
        recovery_date = user_data[15]
        reason_cancel = user_data[16]
        reason_delete = user_data[17]

        text = f"Username tg - {username}\n" \
               f"Тариф подписки - {tariff}\n" \
               f"Подписка до - {sub_term}\n" \
               f"Дата последней оплаты - {payment_date}\n" \
               f"Имя - {name}\n" \
               f"Фамилия - {surname}\n" \
               f"Инстаграм - {instagram}\n" \
               f"Дата рождения - {birthday}\n" \
               f"Город - {city}\n" \
               f"Статус - {status}\n" \
               f"Дата регистрации - {registration_date}\n" \
               f"Дата автоматического удаления - {deleteauto_date}\n" \
               f"Дата отмены подписки пользователем - {cancel_date}\n" \
               f"Дата БАНа пользователя - {ban_date}\n" \
               f"Дата возвращения пользователя - {recovery_date}\n" \
               f"Причина самостоятельной отмены подписки - {reason_cancel}\n" \
               f"Причина БАНа - {reason_delete}"
        await message.answer(text)
    else:
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton("Искать другого пользователя", callback_data="search_user")]
            ]
        )
        await message.answer(f"Пользователя {username} нет", reply_markup=markup)
    await state.finish()


@dp.callback_query_handler(text="instagram_search")
async def search_user_with_instagram(call: CallbackQuery):
    await call.message.edit_text("Введи Instagram-аккаунт (без @)")

    await states.Search.instagram.set()


@dp.message_handler(state=states.Search.instagram)
async def set_username(message: types.Message, state: FSMContext):
    status_type = {
        0: "новый пользователь, зарегался, но не оплатил",
        1: "новый пользователь, оплатил подписку, оплату нужно подтвердить",
        2: "текущий пользователь, подписка оплачена",
        3: "текущий пользователь, подписка истекает",
        4: "текущий пользователь, продлил подписку, оплату нужно подтвердить",
        5: "текущий пользователь сменил тариф, но не оплатил его",
        6: "текущий пользователь сменил тариф, оплатил подписку, оплату нужно подтвердить",
        7: "автоматически удален за неуплату подписки",
        8: "пользователь в БАНе",
        9: "пользователь, отменивший подписку",
        10: "пользователь восстанавливает подписку, но не оплатил",
        11: "пользователь восстанавливает подписку, нужно подтвердить оплату",
        12: "начал процедуру, но решил не оплачивать",
        13: "начал регистрацию, но не завершил её"
    }

    instagram = message.text

    user_data = await db.get_user_with_data(row_name="instagram", data=instagram)

    if user_data:
        username = user_data[0]
        tariff = user_data[1]
        sub_term = user_data[3]
        payment_date = user_data[4]
        name = user_data[5]
        surname = user_data[6]
        instagram = user_data[7]
        birthday = user_data[8]
        city = user_data[9]
        status = status_type[user_data[10]]
        registration_date = user_data[11]
        deleteauto_date = user_data[12]
        cancel_date = user_data[13]
        ban_date = user_data[14]
        recovery_date = user_data[15]
        reason_cancel = user_data[16]
        reason_delete = user_data[17]

        text = f"Username tg - {username}\n" \
               f"Тариф подписки - {tariff}\n" \
               f"Подписка до - {sub_term}\n" \
               f"Дата последней оплаты - {payment_date}\n" \
               f"Имя - {name}\n" \
               f"Фамилия - {surname}\n" \
               f"Инстаграм - {instagram}\n" \
               f"Дата рождения - {birthday}\n" \
               f"Город - {city}\n" \
               f"Статус - {status}\n" \
               f"Дата регистрации - {registration_date}\n" \
               f"Дата автоматического удаления - {deleteauto_date}\n" \
               f"Дата отмены подписки пользователем - {cancel_date}\n" \
               f"Дата БАНа пользователя - {ban_date}\n" \
               f"Дата возвращения пользователя - {recovery_date}\n" \
               f"Причина самостоятельной отмены подписки - {reason_cancel}\n" \
               f"Причина БАНа - {reason_delete}"
        await message.answer(text)
    else:
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton("Искать другого пользователя", callback_data="search_user")]
            ]
        )
        await message.answer(f"Пользователя c инстаграмом '{instagram}' нет", reply_markup=markup)
    await state.finish()
