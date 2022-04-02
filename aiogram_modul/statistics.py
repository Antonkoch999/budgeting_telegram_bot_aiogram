import logging

from aiogram import Dispatcher, types

from aiogram_modul.constants import CommandEnum

logger = logging.getLogger(__name__)


async def statistic_month(message: types.Message):
    """New entry."""
    await message.answer('Statistics')


def register_handlers_statistics(dp: Dispatcher):
    """Register command in this file."""
    dp.register_message_handler(
        statistic_month,
        commands=CommandEnum.STATISTIC_MONTH.value,
    )
