"""Base commands."""

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from aiogram_modul.constants import COMMANDS


def auth(func):
    """Authenticate decorator."""
    async def wrapper(message):
        if message['from']['id'] not in (333252589, 409501763):
            print(f'Пользователь {message["from"]["id"]} '
                  f'пытался воспользоваться ботом!')
            return await message.answer('У вас нет прав '
                                        'работать с этим ботом!')
        return await func(message)

    return wrapper


async def cmd_help(message: types.Message):
    """Help command, display all commands."""
    help_text = "Доступны следующие команды: \n\n"
    for key in COMMANDS:
        help_text += key + ": "
        help_text += COMMANDS[key] + "\n"
    await message.answer(help_text)


async def cmd_start(message: types.Message, state: FSMContext):
    """Start command, display all commands."""
    await state.finish()
    start_text = "Привет. Я бот бюджетирования как я могу тебе помочь?\n\n"
    for key in COMMANDS:
        start_text += key + ": "
        start_text += COMMANDS[key] + "\n"
    await message.answer(start_text, reply_markup=types.ReplyKeyboardRemove())


async def cmd_cancel(message: types.Message, state: FSMContext):
    """Cancel command, return on start page."""
    await state.finish()
    await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())


def register_handlers_common(dp: Dispatcher):
    """Register command in this file."""
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_help, commands="help", state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(cmd_cancel, Text(equals="Отмена", ignore_case=True), state="*")
