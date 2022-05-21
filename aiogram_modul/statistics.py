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
    ChoiceDateType,
    CommandEnum,
    HistoryChoiceEnum,
    StatisticsChoiceEnum,
    StatisticsChoiceMonthEnum,
)
from aiogram_modul.keyboard import choice_variant_statistics, choice_variant_history, choice_variant_month_statistics
from database.base_model import StatisticsBase
from database.db import get_history_by_date, get_statistics_by_date

logger = logging.getLogger(__name__)


class StatisticsState(StatesGroup):
    """Class for state bot."""

    statistics_choice_type = State()
    statistics_choice_month = State()


class HistoryState(StatesGroup):
    """Class for state bot."""

    history_choice = State()


async def history(message: types.Message):
    """Choice variant history."""
    await HistoryState.history_choice.set()
    await message.answer(AnswerEnum.CHOICE_VARIANT_HISTORY.value, reply_markup=choice_variant_history)


async def history_choice(message: types.Message, state: FSMContext):
    """History by date."""
    result = []

    if message.text == BackEnum.BACK.value:
        await state.finish()
        await message.answer(generate_start_text(), reply_markup=types.ReplyKeyboardRemove())
        return
    elif message.text == HistoryChoiceEnum.HISTORY_BY_DAY.value:
        await state.finish()
        result = await get_history_by_date(message.bot['session'], message['from']['id'], ChoiceDateType.DAY)
    elif message.text == HistoryChoiceEnum.HISTORY_BY_MONTH.value:
        await state.finish()
        result = await get_history_by_date(message.bot['session'], message['from']['id'], ChoiceDateType.MONTH)
    elif message.text == HistoryChoiceEnum.HISTORY_BY_YEAR.value:
        await state.finish()
        result = await get_history_by_date(message.bot['session'], message['from']['id'], ChoiceDateType.YEAR)

    table = prettytable.PrettyTable([AnswerEnum.DATE.value, AnswerEnum.CATEGORY.value, AnswerEnum.AMOUNT.value])
    for info in result:
        table.add_row([info.date, info.category_name, round(float(info.amount), 2)])

    await message.answer(
        f'<pre>{table}</pre>',
        parse_mode='HTML',
        reply_markup=types.ReplyKeyboardRemove(),
    )


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


async def statistics(message: types.Message):
    """Choice variant statistics."""
    await StatisticsState.statistics_choice_type.set()
    await message.answer(AnswerEnum.CHOICE_VARIANT_STATISTICS.value, reply_markup=choice_variant_statistics)


async def statistics_choice_type(message: types.Message, state: FSMContext):
    result = []

    if message.text == BackEnum.BACK.value:
        await state.finish()
        await message.answer(generate_start_text(), reply_markup=types.ReplyKeyboardRemove())
        return
    elif message.text == StatisticsChoiceEnum.STATISTICS_BY_DAY.value:
        result = await get_statistics_by_date(message.bot['session'], message['from']['id'], ChoiceDateType.DAY)
    elif message.text == StatisticsChoiceEnum.STATISTICS_BY_MONTH.value:
        await StatisticsState.statistics_choice_month.set()
        await message.answer(
            AnswerEnum.CHOICE_VARIANT_MONTH_STATISTICS.value,
            reply_markup=choice_variant_month_statistics,
        )
        return
    elif message.text == StatisticsChoiceEnum.STATISTICS_BY_YEAR.value:
        result = await get_statistics_by_date(message.bot['session'], message['from']['id'], ChoiceDateType.YEAR)

    table = _prepare_table_for_statistics(result)
    await message.answer(
        f'<pre>{table}</pre>',
        parse_mode='HTML',
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await state.finish()


async def statistics_by_month(message: types.Message, state: FSMContext):
    if message.text == BackEnum.BACK.value:
        await StatisticsState.statistics_choice_type.set()
        await message.answer(AnswerEnum.CHOICE_VARIANT_STATISTICS.value, reply_markup=choice_variant_statistics)
        return

    value_date = StatisticsChoiceMonthEnum(message.text).values[1]
    result = await get_statistics_by_date(
        message.bot['session'],
        message['from']['id'],
        ChoiceDateType.MONTH,
        value_date,
    )
    table = _prepare_table_for_statistics(result)
    await message.answer(
        f'<pre>{table}</pre>',
        parse_mode='HTML',
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await state.finish()


def register_handlers_statistics(dp: Dispatcher):
    """Register command in this file."""
    dp.register_message_handler(
        history,
        commands=CommandEnum.HISTORY.value,
    )
    dp.register_message_handler(
        history_choice,
        state=HistoryState.history_choice,
    )
    dp.register_message_handler(
        statistics,
        commands=CommandEnum.STATISTICS.value,
    )
    dp.register_message_handler(
        statistics_choice_type,
        state=StatisticsState.statistics_choice_type,
    )
    dp.register_message_handler(
        statistics_by_month,
        state=StatisticsState.statistics_choice_month,
    )
