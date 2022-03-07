import asyncio
import datetime
from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, \
    KeyboardButton, BotCommandScopeChat

from keyboards.inline.callback_data import gender_cd, rates_cd, registration_cd
from loader import dp, _, db, bot
from states import states
from utils.mailings import notify_operator
from utils.shedulers.notify_of_payment import notify_of_payment


@dp.callback_query_handler(text="registration_user")
async def start_registrate_user(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await ask_name(call.message, state)


@dp.message_handler(text=["Регистрация", "Registration"])
async def ask_name(message: types.Message, state: FSMContext, callback_data: dict = False, isChange=False):
    async with state.proxy() as data:
        data['isChange'] = isChange

    await message.answer(_("Напишите ваше имя"), reply_markup=types.ReplyKeyboardRemove())
    await states.User.name.set()


@dp.message_handler(state=states.User.name)
async def ask_surname(message: types.Message, state: FSMContext, callback_data: dict = False, isChange=False):
    name = message.text

    async with state.proxy() as data:
        if name != _("Что нужно изменить?"):
            data['name'] = name
        status = data['isChange']
        data['isChange'] = isChange

    if status:
        return await confirm_registration(message, state)

    await message.answer(_("Напишите вашу фамилию"))
    await states.User.surname.set()


@dp.message_handler(state=states.User.surname)
async def ask_instagram(message: types.Message, state: FSMContext, callback_data: dict = False, isChange=False):
    surname = message.text

    async with state.proxy() as data:
        if surname != _("Что нужно изменить?"):
            data['surname'] = surname
        status = data['isChange']
        data['isChange'] = isChange

    if status:
        return await confirm_registration(message, state)

    await message.answer(_("Укажите свой аккаунт в Instagram, без символа @ (если нет, то любую другую соц. сеть)"))
    await states.User.instagram.set()


@dp.message_handler(state=states.User.instagram)
async def ask_birthday(message: types.Message, state: FSMContext, callback_data: dict = False, isChange=False):
    instagram = message.text

    async with state.proxy() as data:
        if instagram != _("Что нужно изменить?"):
            data['instagram'] = instagram
        status = data['isChange']
        data['isChange'] = isChange

    if status:
        return await confirm_registration(message, state)

    await message.answer(_("Дата рождения в формате дд.мм.гггг"))
    await states.User.birthday.set()


@dp.message_handler(state=states.User.birthday)
async def ask_gender(message: types.Message, state: FSMContext, callback_data: dict = False, isChange=False):
    birthday = message.text

    async with state.proxy() as data:
        if birthday != _("Что нужно изменить?"):
            try:
                datetime.datetime.strptime(birthday, '%d.%m.%Y')
            except:
                await message.answer(_("Не правильный формат даты! Формат: дд.мм.гггг"))
                return
            data['birthday'] = birthday
        status = data['isChange']
        data['isChange'] = isChange

    if status:
        return await confirm_registration(message, state)

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=_("Мужской"),
                                  callback_data=gender_cd.new(value=_("Мужской"))),
             InlineKeyboardButton(text=_("Женский"),
                                  callback_data=gender_cd.new(value=_("Женский")))]
        ]
    )

    await message.answer(_("Выберите свой пол"), reply_markup=markup)
    await states.User.gender.set()


@dp.callback_query_handler(gender_cd.filter(), state=states.User.gender)
async def ask_city(call: Union[CallbackQuery, types.Message], callback_data: dict, state: FSMContext, isChange=False):
    gender = callback_data.get("value")

    async with state.proxy() as data:
        if isinstance(call, CallbackQuery):
            data['gender'] = gender
        status = data['isChange']
        data['isChange'] = isChange

    if status:
        if isinstance(call, CallbackQuery):
            await call.message.delete()
        else:
            await bot.delete_message(call.chat.id, call.message_id - 1)
        return await confirm_registration(call.message, state)

    if isinstance(call, CallbackQuery):
        await call.message.edit_reply_markup()
        await call.message.answer(_("Укажите город проживания"))
    else:
        message = call
        await message.answer(_("Укажите город проживания"))

    await states.User.city.set()


@dp.message_handler(state=states.User.city)
async def ask_rates(message: types.Message, state: FSMContext, callback_data: dict = False, isChange=False):
    city = message.text

    async with state.proxy() as data:
        if city != _("Что нужно изменить?"):
            data['city'] = city
        status = data['isChange']
        data['isChange'] = isChange

    if status:
        return await confirm_registration(message, state)

    rates = await db.get_rates()
    print(rates)

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(_("1 месяц") + f"({rates[0][2]}р.)", callback_data=
            rates_cd.new(rate_id=rates[0][0], rate_price=str(rates[0][2]),
                         using_type="0", rate_name="1 месяц"))],
            [InlineKeyboardButton(_("6 месяцев") + f"({rates[1][2]}р.)", callback_data=
            rates_cd.new(rate_id=rates[1][0], rate_price=str(rates[1][2]),
                         using_type="0", rate_name="6 месяцев"))],
            [InlineKeyboardButton(_("12 месяцев") + f"({rates[2][2]}р.)", callback_data=
            rates_cd.new(rate_id=rates[2][0], rate_price=str(rates[2][2]),
                         using_type="0", rate_name="12 месяцев"))]
        ]
    )

    await message.answer(_("Выберите тариф подписки"), reply_markup=markup)
    await states.User.rate.set()


@dp.callback_query_handler(rates_cd.filter(using_type="0"), state=states.User.rate)
async def set_rates(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.delete()
    rate_id = callback_data.get("rate_id")
    rate_price = callback_data.get("rate_price")

    async with state.proxy() as data:
        data["rate_id"] = rate_id
        data["rate_name"] = callback_data.get("rate_name")
        data["rate_price"] = rate_price

    await confirm_registration(call.message, state)


async def confirm_registration(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        name = data["name"]
        surname = data["surname"]
        birthday = data["birthday"]
        instagram = data["instagram"]
        gender = data["gender"]
        city = data['city']
        rate_price = data["rate_price"]
        rate_name = data["rate_name"]
        data['isChange'] = False

    await state.reset_state(with_data=False)

    text = _("Ваше имя: {name}\n"
             "Ваша фамилия: {surname}\n"
             "Аккаунт в Instagram: {instagram}\n"
             "Дата рождения: {birthday}\n"
             "Пол: {gender}\n"
             "Город: {city}\n"
             "Тариф подписки: {rate_name} ({rate_price}р.)").format(name=name, surname=surname, birthday=birthday,
                                                                    rate_price=rate_price,
                                                                    instagram=instagram, gender=gender, city=city,
                                                                    rate_name=rate_name)

    await message.answer(text)

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=_("Да"),
                                  callback_data="yes"),
             InlineKeyboardButton(text=_("Нет"),
                                  callback_data="no")]
        ]
    )

    await message.answer(_("Все верно?"), reply_markup=markup)


@dp.callback_query_handler(text="no")
async def get_change_parameters(call: CallbackQuery):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=_("Имя"), callback_data=registration_cd.new(number="1"))],
            [InlineKeyboardButton(text=_("Фамилия"), callback_data=registration_cd.new(number="2"))],
            [InlineKeyboardButton(text=_("Аккаунт в Instagram"), callback_data=registration_cd.new(number="3"))],
            [InlineKeyboardButton(text=_("Дата рождения"), callback_data=registration_cd.new(number="4"))],
            [InlineKeyboardButton(text=_("Пол"), callback_data=registration_cd.new(number="5"))],
            [InlineKeyboardButton(text=_("Город"), callback_data=registration_cd.new(number="6"))],
            [InlineKeyboardButton(text=_("Тариф подписки"), callback_data=registration_cd.new(number="7"))],
        ]
    )

    await call.message.edit_text(_("Что нужно изменить?"), reply_markup=markup)


@dp.callback_query_handler(registration_cd.filter())
async def change_registration_value(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.delete()

    number = callback_data.get("number")

    levels = {
        "1": ask_name,
        "2": ask_surname,
        "3": ask_instagram,
        "4": ask_birthday,
        "5": ask_gender,
        "6": ask_city,
        "7": ask_rates,
    }

    navigation_function = levels[number]

    await navigation_function(call.message, callback_data=callback_data, state=state, isChange=True)


@dp.callback_query_handler(text="yes")
async def add_user_parameters(call: CallbackQuery, state: FSMContext):
    user_id = call.message.chat.id

    async with state.proxy() as data:
        name = data["name"]
        surname = data["surname"]
        birthday = data["birthday"]
        instagram = data["instagram"]
        gender = data["gender"]
        city = data['city']
        rate_id = data["rate_id"]

    now_datetime = datetime.datetime.now().date()
    birthday_dt = datetime.datetime.strptime(birthday, '%d.%m.%Y')
    birthday_st = datetime.datetime.strftime(birthday_dt, '%Y-%m-%d')

    request = f"rate_id={rate_id}, status=0, name='{name}', surname='{surname}', instagram='{instagram}'," \
              f" gender='{gender}', city='{city}', temp_date='{now_datetime}', birthday='{birthday_st}'"

    await db.add_user_parameters(user_id, request=request)

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=_("Договор-оферты"), url="https://docs.google.com/document/d"
                                                                "/1osEKLE6VPqN2hAAMinOo97woQCpTvNsUs1uZ4G3adCk/edit?usp=sharing")],
            [InlineKeyboardButton(text=_("Правила телеграм-канала 'Пой со мной'"), url="https://docs.google.com"
                                                                                       "/document/d/1N_O8vBd3UfZg6lXV0PIWCV_k2vLrIN0UId4BYi_vheg/edit?usp=sharing")]
        ]
    )

    await call.message.edit_text(
        _("Для завершения регистрации необходимо ознакомиться с договором-оферты и правилами канала"),
        reply_markup=markup)

    await asyncio.sleep(1)

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=_("Да"), callback_data="agreement")]
        ]
    )

    await call.message.answer(
        _("Нажатие кнопки 'Да' означает ваше согласие с условиями договора-оферты и правилами канала"),
        reply_markup=markup)

    await state.finish()


@dp.callback_query_handler(text="agreement")
async def get_parameters_for_payment(call: CallbackQuery, state: FSMContext, isExtension=False, rate_id=False,
                                     want_sub=False):

    asyncio.create_task(notify_of_payment(call.message.chat.id))

    async with state.proxy() as data:
        data["isExtension"] = isExtension
        data["rate_id"] = rate_id
        data["want_sub"] = want_sub

    if rate_id:
        price = await db.get_rate_info(rate_id)
        price = price[2]
    else:
        price = await db.get_rates_info(call.message.chat.id)
        price = price[0]
    card_number = await db.get_card_number()

    await call.message.edit_text(_("Переведите оплату в соответствии с вашим тарифом {price}р. на карту Сбербанка: "
                                   "<code>{card_number}</code>\n"
                                   "(нажмите на номер карты, чтобы скопировать его)\n"
                                   "Получатель: Елизавета Владимировна А.\n"
                                   "После совершения перевода, отправьте сюда скриншот банковской операции\n"
                                   "В ответ вы получите ссылку на телеграм-канал.\n\n"
                                   "❓Если вы не получили сообщение в ответ на отправленный скриншот, напишите нам, "
                                   "мы поможем @QA_support").format(
        price=price, card_number=card_number),
        parse_mode="HTML")

    await states.PaymentPhoto.photo.set()


@dp.message_handler(content_types=types.ContentType.DOCUMENT, state=states.PaymentPhoto.photo)
async def handle_documents(message: types.Message, state: FSMContext):
    payment_screenshot = message.document.file_id
    await finish_registration(message, state, screen=payment_screenshot)


@dp.message_handler(content_types=types.ContentType.PHOTO, state=states.PaymentPhoto.photo)
async def finish_registration(message: types.Message, state: FSMContext, screen=False):
    async with state.proxy() as data:
        isExtension = data["isExtension"]
        rate_id = data["rate_id"]
        want_sub = data['want_sub']

    if screen:
        payment_screenshot = screen
    else:
        payment_screenshot = message.photo[-1].file_id
    user_id = message.chat.id
    username = message.chat.username

    if rate_id:
        rate_term = await db.get_rate_info(rate_id)
        rate_amount = rate_term[2]
        rate_term = rate_term[3]
    else:
        rate_term = await db.get_rates_info(user_id)
        rate_amount = rate_term[0]
        rate_term = rate_term[1]
    channel_link = await db.get_channel_link()

    now_date = datetime.datetime.now().date()
    subscription_date = now_date + datetime.timedelta(days=rate_term)

    request = f"subscription_date='{subscription_date}', payment_date='{now_date}', " \
              f"payment_screen='{payment_screenshot}', payment_amount={rate_amount}"

    if not isExtension:
        notify_type = 0
        payment_type = 0

        if want_sub:
            notify_type = 3
            payment_type = 3
            request += f", rate_id={rate_id}, status=11, temp_date=null, recovery_date='{datetime.datetime.now().date()}'," \
                       f"deleteauto_date=null, cancel_date=null, link=1"
        else:
            request += f", registration_date='{now_date}', offer=true, temp_date=null, status=1, link=1"

        markup = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=_('Меню'))]
            ],
            resize_keyboard=True
        )

        await message.answer(
            _("Спасибо за оплату!\n"
              "Вот ваша персональная ссылка на для входа в телеграм-канал: {link}\n"
              "Внимание! Ссылкой можно воспользоваться только один раз, если ссылка будет передана третьему лицу, "
              "то вы сами в канал войти не сможете, а так же будете добавлены в черный список.\n\n"
              "Для эффективной работы с телеграм-каналом, рекомендуем ознакомиться с методикой освоения материала "
              "https://t.me/c/1614950824/23\n\n"
              "Вы можете вступить в чат канала https://t.me/+mVL7vOP__pdlMmQ6 чтобы найти тех, с кем можно петь в "
              "вашем городе или обсудить материалы канала с участниками.\n\n"
              "У этого  бота есть полезные функции. Например “Поиск песен”. С помощью этой функции вы сможете найти песню по "
              "названию, региону, жанру или уровню сложности.\n"
              "Подробнее о боте вы можете узнать в разделе “Что умеет бот?” (находится в Меню)\n"
              "Приятного прослушивания!").format(link=channel_link), reply_markup=markup)

        await bot.set_my_commands(
            [
                types.BotCommand("menu", "Отобразить меню"),
            ], scope=BotCommandScopeChat(message.chat.id)
        )

    else:
        if rate_id:
            notify_type = 2
            payment_type = 2

            request += f", rate_id={rate_id}, status=6, temp_date=null, link=0"
        else:
            notify_type = 1
            payment_type = 1

            request += ", status=4, link=0"

        await message.answer(_("Спасибо! Рад что вы с нами!"))

    await db.add_user_parameters(user_id, request)

    await notify_operator(user_id, username, notify_type=notify_type, payment_type=payment_type)

    await state.finish()


@dp.message_handler(state=states.PaymentPhoto.photo)
async def require_photo(message: types.Message):
    await message.answer(_("Вы не прикрепили скриншот"))
