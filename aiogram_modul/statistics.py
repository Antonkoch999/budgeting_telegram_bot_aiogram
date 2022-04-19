import logging
import prettytable

from aiogram import Dispatcher, types

from aiogram_modul.constants import CommandEnum, AnswerEnum
from database.db import get_history_month

logger = logging.getLogger(__name__)


async def history_by_month(message: types.Message):
    """New entry."""
    result = await get_history_month(message.bot['session'], message['from']['id'])
    table = prettytable.PrettyTable([AnswerEnum.DATE.value, AnswerEnum.CATEGORY.value, AnswerEnum.AMOUNT.value])
    amount_by_month = 0
    for info in result:
        amount_by_month += info.amount
        table.add_row([info.date, info.category_name, info.amount])

    await message.answer(
        f'<pre>{table}</pre>',
        parse_mode='HTML',
        reply_markup=types.ReplyKeyboardRemove(),
    )


def register_handlers_statistics(dp: Dispatcher):
    """Register command in this file."""
    dp.register_message_handler(
        history_by_month,
        commands=CommandEnum.HISTORY_MONTH.value,
    )
