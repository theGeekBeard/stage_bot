from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp, _


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = _("<b>📋Список команд:</b> \n\n"
             "/start - Начать диалог \n"
             "/help - Получить справку\n"
             "/menu - Отобразить кнопки меню\n\n")

    await message.answer(text, parse_mode="HTML")
