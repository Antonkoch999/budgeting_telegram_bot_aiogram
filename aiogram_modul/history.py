import logging

import prettytable

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from aiogram_modul.base_command import generate_start_text
from aiogram_modul.constants import (
    AnswerEnum,
    BackEnum,
    HistoryChoiceEnum, CommandEnum,
)
from aiogram_modul.help_functions import chunks
from aiogram_modul.keyboard import choice_variant_history, back_keyboard_markup
from database.db import GetBudgetingData

logger = logging.getLogger(__name__)
MAX_SIZE_MESSAGE = 50


class HistoryState(StatesGroup):
    """Class for state bot."""

    history_choice = State()
    history_choice_period = State()


async def history(message: types.Message):
    """Choice variant history."""
    await HistoryState.history_choice.set()
    await message.answer(AnswerEnum.CHOICE_VARIANT_HISTORY.value, reply_markup=choice_variant_history)


async def history_choice(message: types.Message, state: FSMContext):
    """History by date."""
    result = []
    budgeting_data = GetBudgetingData()

    if message.text == BackEnum.BACK.value:
        await state.finish()
        await message.answer(generate_start_text(), reply_markup=types.ReplyKeyboardRemove())
        return
    elif message.text == HistoryChoiceEnum.HISTORY_BY_DAY.value:
        result = await budgeting_data.get_data_budgeting_by_day(message.bot['session'], message['from']['id'])
    elif message.text == HistoryChoiceEnum.HISTORY_BY_MONTH.value:
        result = await budgeting_data.get_data_budgeting_by_month(message.bot['session'], message['from']['id'])
    elif message.text == HistoryChoiceEnum.HISTORY_BY_YEAR.value:
        result = await budgeting_data.get_data_budgeting_by_year(message.bot['session'], message['from']['id'])
    elif message.text == HistoryChoiceEnum.HISTORY_BY_PERIOD.value:
        await HistoryState.history_choice_period.set()
        await message.answer(AnswerEnum.CHOICE_PERIOD.value, reply_markup=back_keyboard_markup)
        return

    table = prettytable.PrettyTable([AnswerEnum.DATE.value, AnswerEnum.CATEGORY.value, AnswerEnum.AMOUNT.value])
    for info in result:
        table.add_row([info.date, info.category_name, info.amount])

    if len(result) > MAX_SIZE_MESSAGE:
        for chunk_list in chunks(result, MAX_SIZE_MESSAGE):
            table = prettytable.PrettyTable([AnswerEnum.DATE.value, AnswerEnum.CATEGORY.value, AnswerEnum.AMOUNT.value])
            for info in chunk_list:
                table.add_row([info.date, info.category_name, info.amount])
            await message.answer(
                f'<pre>{table}</pre>',
                parse_mode='HTML',
                reply_markup=types.ReplyKeyboardRemove(),
            )
    else:
        await message.answer(
            f'<pre>{table}</pre>',
            parse_mode='HTML',
            reply_markup=types.ReplyKeyboardRemove(),
        )
    await state.finish()


async def history_by_period(message: types.Message, state: FSMContext):
    if message.text == BackEnum.BACK.value:
        await HistoryState.history_choice_period.set()
        await message.answer(AnswerEnum.CHOICE_VARIANT_HISTORY.value, reply_markup=choice_variant_history)
        return

    await message.answer(
        'Эта функция в стадии разработки и пока не работает.',
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await state.finish()


def register_handlers_history(dp: Dispatcher):
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
        history_by_period,
        state=HistoryState.history_choice_period,
    )
