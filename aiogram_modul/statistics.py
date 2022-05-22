import logging
from typing import List

import prettytable

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from aiogram_modul.base_command import generate_start_text
from aiogram_modul.constants import (
    AnswerEnum,
    BackEnum,
    CommandEnum,
    StatisticsChoiceEnum,
)
from aiogram_modul.keyboard import choice_variant_statistics, back_keyboard_markup
from database.base_model import StatisticsBase
from database.db import GetBudgetingData

logger = logging.getLogger(__name__)


class StatisticsState(StatesGroup):
    """Class for state bot."""

    statistics_choice_type = State()
    statistics_choice_period = State()


def _prepare_table_for_statistics(result: List[StatisticsBase]):
    """Prepare table for answer."""
    table = prettytable.PrettyTable([AnswerEnum.CATEGORY.value, AnswerEnum.AMOUNT.value])
    total_amount = 0
    for info in sorted(result, key=lambda category: category.amount, reverse=True):
        total_amount += info.amount
        table.add_row([info.category_name, round(float(info.amount), 2)])
    table.add_row(['-----------', '-------'])
    table.add_row([AnswerEnum.TOTAL.value, round(float(total_amount), 2)])
    return table


def _group_statistics_by_category(result: List[StatisticsBase]) -> List[StatisticsBase]:
    category_amount = {}
    for data in result:
        if category_amount.get(data.category_name):
            category_amount[data.category_name] += data.amount
        else:
            category_amount[data.category_name] = data.amount
    return [
        StatisticsBase(category_name=category_name, amount=amount)
        for category_name, amount in category_amount.items()
    ]


async def statistics(message: types.Message):
    """Choice variant statistics."""
    await StatisticsState.statistics_choice_type.set()
    await message.answer(AnswerEnum.CHOICE_VARIANT_STATISTICS.value, reply_markup=choice_variant_statistics)


async def statistics_choice_type(message: types.Message, state: FSMContext):
    result = []
    budgeting_data = GetBudgetingData()

    if message.text == BackEnum.BACK.value:
        await state.finish()
        await message.answer(generate_start_text(), reply_markup=types.ReplyKeyboardRemove())
        return
    elif message.text == StatisticsChoiceEnum.STATISTICS_BY_DAY.value:
        result = await budgeting_data.get_data_budgeting_by_day(
            message.bot['session'],
            message['from']['id'],
        )
    elif message.text == StatisticsChoiceEnum.STATISTICS_BY_MONTH.value:
        result = await budgeting_data.get_data_budgeting_by_month(
            message.bot['session'],
            message['from']['id'],
        )
    elif message.text == StatisticsChoiceEnum.STATISTICS_BY_YEAR.value:
        result = await budgeting_data.get_data_budgeting_by_year(
            message.bot['session'],
            message['from']['id'],
        )
    elif message.text == StatisticsChoiceEnum.STATISTICS_BY_PERIOD.value:
        await StatisticsState.statistics_choice_period.set()
        await message.answer(AnswerEnum.CHOICE_PERIOD.value, reply_markup=back_keyboard_markup)
        return

    group_by_category_result = _group_statistics_by_category(result)
    table = _prepare_table_for_statistics(group_by_category_result)
    await message.answer(
        f'<pre>{table}</pre>',
        parse_mode='HTML',
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await state.finish()


async def statistics_by_period(message: types.Message, state: FSMContext):
    if message.text == BackEnum.BACK.value:
        await StatisticsState.statistics_choice_type.set()
        await message.answer(AnswerEnum.CHOICE_VARIANT_STATISTICS.value, reply_markup=choice_variant_statistics)
        return

    await message.answer(
        'Эта функция в стадии разработки и пока не работает.',
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await state.finish()


def register_handlers_statistics(dp: Dispatcher):
    """Register command statistics."""
    dp.register_message_handler(
        statistics,
        commands=CommandEnum.STATISTICS.value,
    )
    dp.register_message_handler(
        statistics_choice_type,
        state=StatisticsState.statistics_choice_type,
    )
    dp.register_message_handler(
        statistics_by_period,
        state=StatisticsState.statistics_choice_period,
    )
