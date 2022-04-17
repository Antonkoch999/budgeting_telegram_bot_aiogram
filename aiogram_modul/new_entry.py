"""Create new entry."""
import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils import markdown

from aiogram_modul.base_command import generate_start_text
from aiogram_modul.constants import (
    AnswerEnum,
    BackEnum,
    IncomeExpenseEnum,
)
from database.db import write_budgeting, get_categories_by_user
from aiogram_modul.keyboard import (
    back_keyboard_markup,
    income_and_expense_markup,
)
from aiogram_modul.help_functions import check_is_digit


logger = logging.getLogger(__name__)


class BudgetingState(StatesGroup):
    """Class for state bot."""

    income_and_expense = State()
    category = State()
    summa = State()


async def new_entry(message: types.Message):
    """New entry."""
    await BudgetingState.income_and_expense.set()
    logger.info("Set state income_and_expense")
    await message.answer(AnswerEnum.ANSWER_INCOME_EXPENSE.value, reply_markup=income_and_expense_markup)


async def choice_income_or_expense(message: types.Message, state: FSMContext):
    """Choice category or enter sum income."""
    if message.text == BackEnum.BACK.value:
        await state.finish()
        await message.answer(generate_start_text(), reply_markup=types.ReplyKeyboardRemove())
        return

    user_categories = await get_categories_by_user(
        message.bot['session'],
        message['from']['id'],
        expense=bool(message.text == IncomeExpenseEnum.EXPENSE.value),
    )
    category_income_expense_markup = ReplyKeyboardMarkup(resize_keyboard=True).add(
        *user_categories
    ).row(BackEnum.BACK.value)
    if message.text in IncomeExpenseEnum.list_value():
        await state.update_data(income_or_expense=message.text)
        await state.update_data(user_categories=user_categories)
        await BudgetingState.category.set()
        await message.answer(
            AnswerEnum.CHOICE_CATEGORY.value.format(message_text=message.text),
            reply_markup=category_income_expense_markup,
        )


async def choice_category(message: types.Message, state: FSMContext):
    if message.text == BackEnum.BACK.value:
        await BudgetingState.income_and_expense.set()
        await message.answer(
            AnswerEnum.ANSWER_INCOME_EXPENSE.value,
            reply_markup=income_and_expense_markup,
        )
        return

    await state.update_data(category_income_or_expense=message.text)
    await BudgetingState.summa.set()
    await message.answer(
        AnswerEnum.SET_AMOUNT.value.format(message_text=message.text),
        reply_markup=back_keyboard_markup,
    )


async def enter_amount_income_or_expense(message: types.Message, state: FSMContext):
    """Enter amount income or expense."""
    if message.text == BackEnum.BACK.value:
        state_data = await state.get_data()
        user_categories = state_data['user_categories']
        category_income_expense_markup = ReplyKeyboardMarkup(resize_keyboard=True).add(
            *user_categories
        ).row(BackEnum.BACK.value)
        await BudgetingState.category.set()
        await message.answer(
            AnswerEnum.CHOICE_CATEGORY.value.format(message_text=state_data['income_or_expense']),
            reply_markup=category_income_expense_markup,
        )
        return

    async with state.proxy() as data:
        summa_is_number = check_is_digit(message.text.replace(',', '.'))
        if summa_is_number:
            data['amount'] = summa_is_number
            username = message.from_user.username
            income_expense_for_db = data['income_or_expense']
            category_for_db = data['category_income_or_expense']
            amount_for_db = data['amount']
            await write_budgeting(message.bot['session'], message['from']['id'], category_for_db, amount_for_db)
            await message.answer(
                markdown.text(
                    markdown.text(markdown.hitalic(AnswerEnum.DATA_RECORDED.value)),
                    markdown.text(
                        AnswerEnum.NAME.value,
                        markdown.hunderline(username),
                    ),
                    markdown.text(f"{AnswerEnum.CHAPTER.value} {income_expense_for_db}"),
                    markdown.text(f"{AnswerEnum.CATEGORY.value} {category_for_db}"),
                    markdown.text(
                        AnswerEnum.AMOUNT.value,
                        markdown.hbold(f'{amount_for_db}'),
                        AnswerEnum.BYN.value,
                    ),
                    sep="\n",
                ),
                parse_mode="HTML",
                reply_markup=types.ReplyKeyboardRemove(),
            )
        else:
            await message.answer(AnswerEnum.INCORRECT_AMOUNT.value)
            return

        await state.finish()


def register_handlers_new_entry(dp: Dispatcher):
    """Register command in this file."""
    dp.register_message_handler(
        new_entry,
        state='*',
        commands='new',
    )
    dp.register_message_handler(
        choice_income_or_expense,
        state=BudgetingState.income_and_expense,
    )
    dp.register_message_handler(
        choice_category,
        state=BudgetingState.category,
    )
    dp.register_message_handler(
        enter_amount_income_or_expense,
        state=BudgetingState.summa,
    )
