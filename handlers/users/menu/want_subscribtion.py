from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup

from handlers.users.markup_handlers import get_tariffs_markup
from loader import dp, _, db


@dp.callback_query_handler(text="want_subscription")
async def want_subscription(call: CallbackQuery, state: FSMContext):
    status = await db.get_user_status(call.message.chat.id)

    tariff = await db.get_rates_info(call.message.chat.id)
    if tariff:
        tariff_name = tariff[-1]

    names = {
        1: "1 месяц",
        2: "6 месяцев",
        3: "12 месяцев"
    }

    sub_date = await db.get_sub_date(call.message.chat.id)

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(_("Вернуться в меню"), callback_data="menu")]
    ])

    if status in (1, 2, 3, 4, 5, 6, 11):
        await call.message.edit_text(
            _("У вас уже есть подписка на {tariff}\n"
              "Ваша подписка действительна до {term}").format(tariff=names[tariff_name], term=sub_date),
            reply_markup=markup)
    elif status == 8:
        await call.message.edit_text(
            _("К сожалению, вы больше не можете пользоваться функциями бота."), reply_markup=None)
    elif status in (13, 0):
        await call.message.edit_text(
            _("У вас не завершен процесс регистрации"), reply_markup=markup)
    elif status == 10:
        await call.message.edit_text(
            _("У вас не завершен процесс смены тарифа подписки"), reply_markup=markup)
    elif status == 12:
        reg_markup = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=_('Регистрация'))]
            ],
            resize_keyboard=True
        )
        await db.add_user_parameters(user_id=call.message.chat.id, request="status=13")
        await call.message.delete()
        await call.message.answer(
            _("Я рад, что вы решили к нам присоединиться. "
              "Для начала, нужно зарегистрировать вас. "
              "Нажимайте кнопку “Регистрация” и начнем"), reply_markup=reg_markup)
    else:
        await call.message.delete()
        await call.message.answer(
            _("Привет, {name}! Я рад, что вы возвращаетесь к нам! Выберите тариф подписки.").format(
                name=call.message.chat.full_name
            ))
        await get_tariffs_markup(call, state=state, want_sub=True)
