from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from loader import dp, _, db


@dp.callback_query_handler(text="can_bot")
async def can_bot(call: CallbackQuery):
    status = await db.get_user_status(call.message.chat.id)

    if status == 8:
        await call.message.edit_text(
            _("К сожалению, вы больше не можете пользоваться функциями бота."), reply_markup=None)
    else:
        text = _(
            """Этот бот создан для того, чтобы вам было удобнее пользоваться телеграмм-каналом 'Пой со мной'.
Бот поможет с оформлением подписки, а также напомнит вам о необходимости продлить подписку.

С помощью кнопки 'Поиск песен' вы сможете найти интересующую вас песню по региону, жанру или уровню сложности.
В случае отсутствия искомой песни, вы можете 'Предложить песню', а мы постараемся добавить ее на канал.
Если вам нужна расшифровка песни, жмите на кнопку 'Хочу расшифровку песни'. Мы сделаем для вас индивидуальную расшифровку любой песни (не входит в стоимость подписки и оплачивается отдельно).
При нажатии кнопки 'Задать вопрос' бот соединит вас с администратором канала
Для оформления подписки на канал есть кнопка 'Хочу подписку'
""")

        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(_("Вернуться в меню"), callback_data="menu")]
        ])

        await call.message.edit_text(text, reply_markup=markup)
