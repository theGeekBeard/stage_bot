import asyncio
from datetime import datetime, timedelta

import pytz
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import bot, db, _
from utils.mailings import notify_operator_about_delete_user


async def check_access():
    while True:
        if datetime.now(pytz.timezone('Europe/Moscow')).hour == 22 and datetime.now(pytz.timezone('Europe/Moscow')).minute == 26:
            print(1)
            text = _("Привет, {name}! Сообщаю, что пора продлить вашу подписку на "
                     "телеграм-канал 'Пой со мной'. До окончания подписки осталось всего {day}. Сейчас у вас "
                     "подписка с тарифом: {rate_name} ({price}р.). Кстати, сейчас вы можете сменить тариф "
                     "подписки.")

            rate_name = {
                1: _("1 месяц"),
                2: _("6 месяцев"),
                3: _("12 месяцев")
            }

            for items in await db.get_users():
                if items[1] == datetime.now().date():
                    print(235)
                    text_del = _("Привет, {name}! Сегодня у вас истек срок подписки на телеграм-канал “Пой со мной”. Мы, "
                             "я вынуждены удалить вас из канала, за то что вы не продлили подписку, таковы правила. В "
                             "любой момент вы можете вернуться к нам. Для этого  нажмите “Хочу подписку” в Меню. Буду "
                             "ждать вас!").format(name=items[2])

                    request = f"status=7, deleteauto_date='{datetime.now().date()}', " \
                              f"recovery_date=null, rate_id=null, subscription_date=null"

                    await db.add_user_parameters(items[0], request)

                    await bot.send_message(items[0], text=text_del)

                    await notify_operator_about_delete_user(items[0], items[-1])

                elif items[1] - timedelta(3) == datetime.now().date():
                    print(2)
                    await db.update_user_parameters(user_id=items[0], parameter_name="status", parameter_value=3)

                    rate = await db.get_rates_info(items[0])

                    markup = InlineKeyboardMarkup(
                        inline_keyboard=[
                            [InlineKeyboardButton(text=_("Оплатить текущий тариф"), callback_data="pay")],
                            [InlineKeyboardButton(text=_("Узнать про все тарифы"), callback_data="about")],
                            [InlineKeyboardButton(text=_("Отказаться от подписки"), callback_data="cancel_sub")]
                        ]
                    )

                    await bot.send_message(items[0],
                                           text=_("Привет, {name}! Сообщаю, что пора продлить вашу подписку на "
                     "телеграм-канал 'Пой со мной'. До окончания подписки осталось всего {day}. Сейчас у вас "
                     "подписка с тарифом: {rate_name} ({price}р.). Кстати, сейчас вы можете сменить тариф "
                     "подписки.").format(name=items[2], day="3 дня", rate_name=rate_name[rate[-1]],
                                                            price=rate[0]),
                                           reply_markup=markup)
                elif items[1] - timedelta(2) == datetime.now().date():
                    print(3)
                    markup = InlineKeyboardMarkup(
                        inline_keyboard=[
                            [InlineKeyboardButton(text=_("Оплатить текущий тариф"), callback_data="pay")],
                            [InlineKeyboardButton(text=_("Узнать про все тарифы"), callback_data="about")],
                            [InlineKeyboardButton(text=_("Отказаться от подписки"), callback_data="cancel_sub")]
                        ]
                    )

                    rate = await db.get_rates_info(items[0])

                    await bot.send_message(items[0],
                                           text=_("Привет, {name}! Сообщаю, что пора продлить вашу подписку на "
                     "телеграм-канал 'Пой со мной'. До окончания подписки осталось всего {day}. Сейчас у вас "
                     "подписка с тарифом: {rate_name} ({price}р.). Кстати, сейчас вы можете сменить тариф "
                     "подписки.").format(name=items[2], day="2 дня", rate_name=rate_name[rate[-1]],
                                                            price=rate[0]),
                                           reply_markup=markup)
                elif items[1] - timedelta(1) == datetime.now().date():
                    print(4)
                    markup = InlineKeyboardMarkup(
                        inline_keyboard=[
                            [InlineKeyboardButton(text=_("Оплатить текущий тариф"), callback_data="pay")],
                            [InlineKeyboardButton(text=_("Узнать про все тарифы"), callback_data="about")],
                            [InlineKeyboardButton(text=_("Отказаться от подписки"), callback_data="cancel_sub")]
                        ]
                    )

                    rate = await db.get_rates_info(items[0])

                    await bot.send_message(items[0],
                                           text=_("Привет, {name}! Сообщаю, что пора продлить вашу подписку на "
                     "телеграм-канал 'Пой со мной'. До окончания подписки осталось всего {day}. Сейчас у вас "
                     "подписка с тарифом: {rate_name} ({price}р.). Кстати, сейчас вы можете сменить тариф "
                     "подписки.").format(name=items[2], day="1 день", rate_name=rate_name[rate[-1]],
                                                            price=rate[0]),
                                           reply_markup=markup)
                else:
                    await asyncio.sleep(60)
            else:
                await asyncio.sleep(60)
        else:
            await asyncio.sleep(60)
