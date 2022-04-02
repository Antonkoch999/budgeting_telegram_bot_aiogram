import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup


logger = logging.getLogger(__name__)


class StatisticState(StatesGroup):
    """Class for state bot."""

    statistic_state = State()
    statistic_category_state = State()


async def statistics(message: types.Message):
    """New entry."""
    await StatisticState.statistic_state.set()
    logger.info("Set state statistic_state")
    await message.answer('Statistics')


def register_handlers_statistics(dp: Dispatcher):
    """Register command in this file."""
    dp.register_message_handler(
        statistics,
        state='*',
        commands='statistic',
    )
