import asyncio
from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, \
    KeyboardButton, BotCommandScopeChat

from loader import dp, db, _, tz, bot
from utils.shedulers.notify_of_registration import notify_of_registration


@dp.message_handler(CommandStart())
async def start_dialog(message: types.Message, state: FSMContext):
    await bot.delete_my_commands(scope=BotCommandScopeChat(message.chat.id))

    admins = await db.get_admins(message.chat.id)

    if admins or message.chat.id == 5294530966:
        markup = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='Действия'),
                 KeyboardButton(text='Меню')]
            ], resize_keyboard=True
        )

        return await message.answer(f"Добро пожаловать в панель администратора\n"
                                    f"Дата и время сервера: {datetime.now(tz)}", reply_markup=markup)

    if message.chat.username is None:
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=_("Как указать username на компьютере?"),
                                      callback_data="get_instruction")],
                [InlineKeyboardButton(text=_("Как указать username на Android?"),
                                      callback_data="get_instruction_android")],
                [InlineKeyboardButton(text=_("Как указать username на iPhone?"),
                                      callback_data="get_instruction_apple")]
            ]
        )

        await message.answer(
            _("Чтобы пользоваться этим ботом вам необходимо указать ваш username в настройках телеграм."),
            reply_markup=markup)
    else:
        await registrate_user(message, state)


@dp.callback_query_handler(text="get_instruction_apple")
async def get_instruction_apple(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()

    temp = 0
    instruction_text = {
        1: _(
            "1. Нажать на кнопку “Настройки” в правом нижнем углу экрана"),
        2: _("2. Нажать на поле “Выбрать имя пользователя”"),
        3: _("3. Ввести имя пользователя и нажать “Готово”")
    }

    images = await db.get_config_value("apple")

    for photo in images:
        temp += 1
        await call.message.answer_photo(photo=photo, caption=instruction_text[temp])

    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=_('Начать'))]
        ],
        resize_keyboard=True
    )

    await call.message.answer(_("После того как укажите username нажмите 'Начать'"),
                              reply_markup=markup)


@dp.callback_query_handler(text="get_instruction_android")
async def get_instruction_android(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()

    temp = 0
    instruction_text = {
        1: _(
            "1. Нажать на значок с тремя полосками в левом верхнем углу экрана"),
        2: _("2. Нажать на кнопку “Настройки”"),
        3: _("3. Нажать в поле “Имя пользователя”"),
        4: _("4. Ввести username и нажать на галочку")
    }

    images = await db.get_config_value("android")
    for photo in images:
        temp += 1
        await call.message.answer_photo(photo=photo, caption=instruction_text[temp])

    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=_('Начать'))]
        ],
        resize_keyboard=True
    )

    await call.message.answer(_("После того как укажите username нажмите 'Начать'"),
                              reply_markup=markup)


@dp.callback_query_handler(text="get_instruction")
async def get_instruction(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()

    temp = 0
    instruction_text = {
        1: _("1. Нажать на значок с тремя полосками в левом верхнем углу экрана\nНажать на кнопку “Настройки”"),
        2: _("2. Нажать на кнопку “Изменить профиль”"),
        3: _("3. Нажать на кнопку “Выбрать имя пользователя”"),
        4: _("4. Ввести username и нажать “Сохранить”")
    }

    images = await db.get_config_value("username_instruction")
    for photo in images:
        temp += 1
        await call.message.answer_photo(photo=photo, caption=instruction_text[temp])

    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=_('Начать'))]
        ],
        resize_keyboard=True
    )

    await call.message.answer(_("После того как укажите username нажмите 'Начать'"),
                              reply_markup=markup)


@dp.message_handler(text=["Начать", "To begin"])
async def registrate_user(message: types.Message, state: FSMContext):
    if message.chat.username is None:
        await message.answer(_("Вы не указали username. \nЕсли у вас возникли трудности, напишите нам, мы поможем "
                               "@lisaveta_suppor"))
        return

    asyncio.create_task(notify_of_registration(message.chat.id))

    user_id = message.chat.id
    username = message.chat.username
    status = 13

    try:
        await db.register_new_user(user_id=user_id, username=username, status=status)
        await db.add_user_parameters(user_id=user_id, request="payment_amount = 0")
    except:
        return await message.answer(_("Произошла ошибка, попробуйте заново, нажав /start"))

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(_('Регистрация'), callback_data="registration_user")]
        ]
    )

    await message.answer(
        _("👋 Привет! Спасибо за интерес к телеграм-каналу “Пой со мной”.\n"
          "❓ Если у вас появятся вопросы в процессе регистрации - напишите нам, мы поможем @QA_support\n\n"
          "⬇️ Нажимайте на кнопку “Регистрация” и начнем"),
        reply_markup=markup)
