"""Base commands."""

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from aiogram_modul.constants import HELP_COMMANDS, START_COMMANDS, AnswerEnum, CommandEnum
from database.db import get_all_user_telegram_id, create_new_user


def _set_help_commands(text: str, type_start: bool = False) -> str:
    commands = START_COMMANDS if type_start else HELP_COMMANDS
    for key in commands:
        text += key + ": "
        text += commands[key] + "\n"
    return text


def generate_start_text() -> str:
    return _set_help_commands(AnswerEnum.START_HEADER.value, type_start=True)


async def cmd_help(message: types.Message):
    """Help command, display all commands."""
    help_text = _set_help_commands(AnswerEnum.HELP_HEADER.value)
    await message.answer(help_text)


async def cmd_start(message: types.Message, state: FSMContext):
    """Start command, display all commands."""
    async_session = message.bot['session']
    username = message.from_user.username
    telegram_id = message.from_user.id
    locale = message.from_user.locale.language
    telegram_ids = await get_all_user_telegram_id(async_session)
    start_text = generate_start_text()

    if telegram_id not in telegram_ids:
        new_user = AnswerEnum.NEW_USER.value.format(username=username) + start_text
        await create_new_user(async_session, telegram_id, username, locale)
        await message.answer(new_user, reply_markup=types.ReplyKeyboardRemove())
        return

    await state.finish()
    await message.answer(start_text, reply_markup=types.ReplyKeyboardRemove())


async def cmd_cancel(message: types.Message, state: FSMContext):
    """Cancel command, return on start page."""
    await state.finish()
    await message.answer(AnswerEnum.CANCEL_MESSAGE.value, reply_markup=types.ReplyKeyboardRemove())


def register_handlers_common(dp: Dispatcher):
    """Register command in this file."""
    dp.register_message_handler(cmd_start, commands=CommandEnum.START.value, state="*")
    dp.register_message_handler(cmd_help, commands=CommandEnum.HELP.value, state="*")
    dp.register_message_handler(cmd_cancel, commands=CommandEnum.CANCEL.value, state="*")
    dp.register_message_handler(cmd_cancel, Text(equals="Отмена", ignore_case=True), state="*")
