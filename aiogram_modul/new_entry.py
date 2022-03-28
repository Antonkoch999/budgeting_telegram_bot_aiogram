"""Create new entry."""
import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import markdown
from aiogram_modul.constants import (
    ANSWER_NEW_ENTRY,
    INCOME_AND_EXPENSE_LIST,
    TEXT_FOR_BUTTON_BACK,
    USER_IDS,
)
from aiogram_modul.db import write_budgeting
from aiogram_modul.keyboard import (
    back_keyboard,
    user_key_board,
    income_and_expense,
    category_income,
    category_expense,
)
from aiogram_modul.help_functions import check_is_digit


logger = logging.getLogger(__name__)


class BudgetingState(StatesGroup):
    """Class for state bot."""

    name = State()
    income_and_expense = State()
    category = State()
    summa = State()


async def new_entry(message: types.Message):
    """New entry."""
    await BudgetingState.name.set()
    logger.info("Set state name")
    await message.answer(ANSWER_NEW_ENTRY, reply_markup=user_key_board)


async def choice_user(message: types.Message, state: FSMContext):
    """Choice income or expense."""
    if USER_IDS.get(message['from']['id']) != message.text:
        await message.answer('У вас нет доступа!')
        return

    await state.update_data(name_user=message.text)
    await BudgetingState.income_and_expense.set()
    logger.info("Set state income and expense")
    await message.answer('Вы хотите записать доход или расход?', reply_markup=income_and_expense)


async def choice_income_or_expense(message: types.Message, state: FSMContext):
    """Choice category or enter sum income."""
    if message.text == TEXT_FOR_BUTTON_BACK:
        await BudgetingState.name.set()
        await message.answer(ANSWER_NEW_ENTRY, reply_markup=user_key_board)
        return

    if message.text not in INCOME_AND_EXPENSE_LIST:
        await message.answer('Пожалуйста, выберите что вы хотите записать, доход или расход?')
        return

    await state.update_data(income_or_expense=message.text)
    await BudgetingState.category.set()
    await message.answer(
        f'Выберите категорию из категории {message.text}:',
        reply_markup=category_income if message.text == 'Доход' else category_expense,
    )


async def choice_category(message: types.Message, state: FSMContext):
    if message.text == TEXT_FOR_BUTTON_BACK:
        await BudgetingState.income_and_expense.set()
        await message.answer(
            'Вы хотите записать доход или расход?',
            reply_markup=income_and_expense,
        )
        return

    await state.update_data(category_income_or_expense=message.text)
    await BudgetingState.summa.set()
    await message.answer(
        f'Введите сумму категории: {message.text} в BYN:',
        reply_markup=back_keyboard,
    )


async def enter_amount_income_or_expense(message: types.Message, state: FSMContext):
    """Enter amount income or expense."""
    if message.text == TEXT_FOR_BUTTON_BACK:
        await BudgetingState.category.set()
        await message.answer(
            f'Выберите категорию {message.text}:',
            reply_markup=category_income if message.text == 'Доход' else category_expense,
        )
        return

    async with state.proxy() as data:
        summa_is_number = check_is_digit(message.text.replace(',', '.'))
        if summa_is_number:
            data['amount'] = summa_is_number
            name_for_db = data.get(
                "name_user",
                "Аноним",
            )
            income_expense_for_db = data.get(
                "income_or_expense",
                "Не понятно что",
            )
            category_for_db = data.get(
                "category_income_or_expense",
                "Зарплата.",
            )
            amount_for_db = data.get(
                "amount",
                "Сумма не указана",
            )
            write_budgeting(message['from']['id'], category_for_db, amount_for_db)
            await message.answer(
                markdown.text(
                    markdown.text(markdown.hitalic("Данные записаны!")),
                    markdown.text(
                        "Имя: ",
                        markdown.hunderline(f"{name_for_db}"),
                    ),
                    markdown.text(f"Раздел: {income_expense_for_db}"),
                    markdown.text(f"Категория: {category_for_db}"),
                    markdown.text(
                        "Сумма: ",
                        markdown.hbold(f'{amount_for_db}'),
                        "BYN",
                    ),
                    sep="\n",
                ),
                parse_mode="HTML",
                reply_markup=types.ReplyKeyboardRemove(),
            )
        else:
            await message.answer('Некорретный формат ввода суммы, '
                                 'попробуйте снова!. Пример: 25.37')
            return
        await state.finish()


def register_handlers_budgeting(dp: Dispatcher):
    """Register command in this file."""
    dp.register_message_handler(
        new_entry,
        state='*',
        commands='new',
    )
    dp.register_message_handler(
        choice_user,
        state=BudgetingState.name,
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
