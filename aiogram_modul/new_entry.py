"""Create new entry."""

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import markdown
from aiogram_modul.constants import COMMANDS
from aiogram_modul.keyboard import (
    user_key_board,
    income_and_expense,
    category_income,
    category_expense,
    user_key_board_list,
    income_and_expense_list,
    category_income_list,
    category_expense_list,
)
from aiogram_modul.bussiness_logic import check_is_digit, write_entry


class BudgetingState(StatesGroup):
    """Class for state bot."""

    name = State()
    income_and_expense = State()
    category = State()
    summa = State()


async def name_user(message: types.Message):
    """Choice user."""
    await BudgetingState.name.set()
    await message.answer('Как вас зовут?', reply_markup=user_key_board)


async def func_income_and_expense(message: types.Message, state: FSMContext):
    """Choice income or expense."""
    if message.text == 'Отмена':
        await state.finish()
        start_text = "Выберите действие\n\n"
        for key in COMMANDS:
            start_text += key + ": "
            start_text += COMMANDS[key] + "\n"
        await message.answer(start_text, reply_markup=types.ReplyKeyboardRemove())
        return

    if message.text not in user_key_board_list:
        await message.answer("Пожалуйста, выберите кто вы, используя клавиатуру ниже.")
        return
    if message.text == 'Кристина' and message['from']['id'] == 409501763:
        await message.answer('У вас нет доступа!')
        return
    if message.text == 'Антон' and message['from']['id'] == 333252589:
        await message.answer('У вас нет доступа!')
        return

    await state.update_data(name_user=message.text)
    await BudgetingState.income_and_expense.set()
    await message.answer('Вы хотите записать доход или расход?', reply_markup=income_and_expense)


async def category(message: types.Message, state: FSMContext):
    """Choice category or enter sum income."""
    if message.text == 'Назад':
        await BudgetingState.name.set()
        await message.answer('Как вас зовут?', reply_markup=user_key_board)
        return

    if message.text not in income_and_expense_list:
        await message.answer('Пожалуйста, выберите что вы хотите записать, доход или расход?')
        return

    if message.text == 'Доход' and message['from']['id'] == 333252589:
        await state.update_data(income_or_expense=message.text)
        await BudgetingState.summa.set()
        await message.answer(
            'Введите сумму дохода в BYN:',
            reply_markup=types.ReplyKeyboardRemove(),
        )

    if message.text == 'Доход' and message['from']['id'] == 409501763:
        await state.update_data(income_or_expense=message.text)
        await BudgetingState.category.set()
        await message.answer(
            'Выберите категорию дохода:',
            reply_markup=category_income,
        )

    if message.text == 'Расход':
        await state.update_data(income_or_expense=message.text)
        await BudgetingState.category.set()
        await message.answer(
            'Выберите категорию расхода:',
            reply_markup=category_expense,
        )


async def summa(message: types.Message, state: FSMContext):
    """Enter summa expense."""
    async with state.proxy() as data:
        condition_user_anton = all([
            message.text == 'Назад',
            data['income_or_expense'] == 'Доход',
            message['from']['id'] == 409501763,
        ])
        condition_user_kristina = all([
            message.text == 'Назад',
            data['income_or_expense'] == 'Доход',
            message['from']['id'] == 333252589,
        ])
        condition_income = all([
            message.text == 'Назад',
            data['income_or_expense'] == 'Расход',
        ])
        if any([
                condition_user_anton,
                condition_user_kristina,
                condition_income,
        ]):
            await BudgetingState.income_and_expense.set()
            await message.answer(
                'Вы хотите записать доход или расход?',
                reply_markup=income_and_expense,
            )
            return

        if message.text in category_income_list:
            await state.update_data(category_income_or_expense=message.text)
            await BudgetingState.summa.set()
            await message.answer(
                'Введите сумму дохода в BYN:',
                reply_markup=types.ReplyKeyboardRemove(),
            )
        elif message.text in category_expense_list:
            await state.update_data(category_income_or_expense=message.text)
            await BudgetingState.summa.set()
            await message.answer(
                'Введите сумму расхода в BYN:',
                reply_markup=types.ReplyKeyboardRemove(),
            )
        else:
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
                    ), parse_mode="HTML")
                write_entry(
                    name_for_db,
                    income_expense_for_db,
                    category_for_db,
                    amount_for_db,
                )
            else:
                await message.answer('Некорретный формат ввода суммы, '
                                     'попробуйте снова!. Пример: 25.37')
                return
            await state.finish()


def register_handlers_budgeting(dp: Dispatcher):
    """Register command in this file."""
    dp.register_message_handler(
        name_user,
        state='*',
        commands='new',
    )
    dp.register_message_handler(
        func_income_and_expense,
        state=BudgetingState.name,
    )
    dp.register_message_handler(
        category,
        state=BudgetingState.income_and_expense,
    )
    dp.register_message_handler(
        summa,
        state=[BudgetingState.summa, BudgetingState.category],
    )
