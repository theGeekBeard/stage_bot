from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from handlers.users.registration import get_parameters_for_payment
from keyboards.inline.callback_data import rates_cd, confirm_payment_cd
from loader import dp, db, _
from states import states
from utils.mailings import notify_operator_about_reason, notify_operator_about_delete_user


@dp.callback_query_handler(text="pay")
async def pay_subscription(call: CallbackQuery, state: FSMContext):
    await get_parameters_for_payment(call, isExtension=True, state=state)


@dp.callback_query_handler(text="about")
async def show_tariffs_info(call: CallbackQuery):
    rates = await db.get_rates()

    text = f"- {rates[0][1]} ({rates[0][2]}р.)\n" \
           f"- {rates[1][1]} ({rates[1][2]}р.)\n" \
           f"- {rates[2][1]} ({rates[2][2]}р.)"

    text = _("1 месяц - ({price}р.)\n"
             "6 месяцев - ({price2}р.)\n"
             "12 месяцев - ({price3}р.))").format(price=rates[0][2], price2=rates[1][2], price3=rates[2][2])

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=_("Хочу сменить тариф"),
                                  callback_data="change_tariff"),
             InlineKeyboardButton(text=_("Оставить текущий тариф"),
                                  callback_data="no_change_tariff")]
        ]
    )

    await call.message.edit_text(_("Текущие тарифы подписки телеграм-канала 'Пой со мной'\n\n" + text),
                                 reply_markup=markup)


@dp.callback_query_handler(text="change_tariff")
async def get_tariffs_markup(call: CallbackQuery, state: FSMContext, want_sub=False):
    rates = await db.get_rates()

    async with state.proxy() as data:
        data['want_sub'] = want_sub

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(_("1 месяц") + f"({rates[0][2]}р.)", callback_data=
            rates_cd.new(rate_id=rates[0][0], rate_price=str(rates[0][2]),
                         using_type="1", rate_name="1 месяц"))],
            [InlineKeyboardButton(_("6 месяцев") + f"({rates[1][2]}р.)", callback_data=
            rates_cd.new(rate_id=rates[1][0], rate_price=str(rates[1][2]),
                         using_type="1", rate_name="6 месяцев"))],
            [InlineKeyboardButton(_("12 месяцев") + f"({rates[2][2]}р.)", callback_data=
            rates_cd.new(rate_id=rates[2][0], rate_price=str(rates[2][2]),
                         using_type="1", rate_name="12 месяцев"))]
        ]
    )

    if want_sub:
        await call.message.answer(_("Выберите тариф подписки"), reply_markup=markup)
    else:
        await call.message.edit_text(_("Выберите тариф подписки"), reply_markup=markup)


@dp.callback_query_handler(rates_cd.filter(using_type="1"))
async def change_tariff(call: CallbackQuery, callback_data: dict, state: FSMContext):
    rate_id = callback_data.get("rate_id")

    async with state.proxy() as data:
        want_sub = data['want_sub']

    if want_sub:
        request = f"status=10, temp_date='{datetime.now().date()}'"
        await db.add_user_parameters(call.message.chat.id, request)
        await call.message.edit_text(_("Отличный выбор! Осталось оплатить подписку"), reply_markup=None)

        return await get_parameters_for_payment(call, rate_id=rate_id, state=state, want_sub=want_sub)

    if await db.check_tariff(call.message.chat.id, rate_id):
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=_("Выбрать тариф"),
                                      callback_data="change_tariff"),
                 InlineKeyboardButton(text=_("Отменить смену тарифа"),
                                      callback_data="no_change_tariff")]
            ]
        )
        await call.message.edit_text(_("У вас уже подключен этот тариф! Выберите другой"), reply_markup=markup)
    else:
        request = f"status=5, temp_date='{datetime.now().date()}'"
        await db.add_user_parameters(call.message.chat.id, request)

        await call.message.edit_text(_("Отличный выбор! Осталось оплатить подписку"), reply_markup=None)

        await get_parameters_for_payment(call, isExtension=True, rate_id=rate_id, state=state)


@dp.callback_query_handler(text="no_change_tariff")
async def no_change_tariff(call: CallbackQuery):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=_("Оплатить текущий тариф"), callback_data="pay")],
            [InlineKeyboardButton(text=_("Узнать про все тарифы"), callback_data="about")],
            [InlineKeyboardButton(text=_("Отказаться от подписки"), callback_data="cancel_sub")]
        ]
    )

    await call.message.edit_text(_("Выберите:"), reply_markup=markup)


@dp.callback_query_handler(text="cancel_sub")
async def cancel_subscription(call: CallbackQuery):
    request = f"status=9, subscription_date=null, rate_id=null, cancel_date='{datetime.now().date()}', " \
              f"recovery_date=null"

    await db.add_user_parameters(call.message.chat.id, request)

    await notify_operator_about_delete_user(call.message.chat.id, call.message.chat.username, notify_type=1)

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=_("Хорошо, напишу"), callback_data="write")],
            [InlineKeyboardButton(text=_("Не хочу писать"), callback_data="no_write")]
        ]
    )

    await call.message.edit_text(_("Подписка отменена\n\nМы работаем над качеством нашего канала и будем "
                                   "признательны, если вы напишете причину отмены подписки"), reply_markup=markup)


@dp.callback_query_handler(text="no_write")
async def bye_user(call: CallbackQuery):
    await call.message.edit_text(_("Спасибо, что были с нами! В любой момент вы можете вернуться к нам. Для этого "
                                   "нажмите 'Хочу подписку' в Меню. Буду ждать вас!"), reply_markup=None)


@dp.callback_query_handler(text="write")
async def reason_cancellation(call: CallbackQuery):
    await call.message.edit_text(_("Напишите пожалуйста, почему вами было принято решение отменить подписку?"))
    await states.Reason.reason.set()


@dp.message_handler(state=states.Reason.reason)
async def call_bye_user(message: types.Message):
    reason = message.text

    request = f"reason_cancel='{reason}'"
    await db.add_user_parameters(message.chat.id, request)

    await message.answer(_("Спасибо, что были с нами! В любой момент вы можете вернуться к нам. Для этого нажмите "
                           "“Хочу подписку” в Меню. Буду ждать вас!"))

    await notify_operator_about_reason(username=message.chat.username, reason=reason)


@dp.callback_query_handler(confirm_payment_cd.filter())
async def confirm_payment(call: CallbackQuery, callback_data: dict):
    username = callback_data["username"]
    user_id = callback_data["user_id"]

    await db.update_user_parameters(user_id, "status", 2)

    await call.message.edit_reply_markup()
    await call.message.answer("Оплата подтверждена!")
