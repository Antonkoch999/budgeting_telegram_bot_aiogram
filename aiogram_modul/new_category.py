"""Create new category."""
import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import markdown

from aiogram_modul.base_command import generate_start_text
from aiogram_modul.constants import (
    AnswerEnum,
    BackEnum,
    IncomeExpenseEnum,
)
from aiogram_modul.crypto_graphy import EncodeDecodeService
from database.db import write_new_category
from aiogram_modul.keyboard import back_keyboard_markup


logger = logging.getLogger(__name__)


class AddCategoryState(StatesGroup):
    """Class for state bot."""

    category = State()


async def add_category(message: types.Message):
    """New entry."""
    await AddCategoryState.category.set()
    logger.info("Set state category")
    await message.answer(
        AnswerEnum.SET_CATEGORY.value,
        reply_markup=back_keyboard_markup,
    )


async def enter_name_category(message: types.Message, state: FSMContext):
    """Enter amount income or expense."""
    if message.text == BackEnum.BACK.value:
        await state.finish()
        await message.answer(generate_start_text(), reply_markup=types.ReplyKeyboardRemove())
        return

    expense = True
    encode_category_name = EncodeDecodeService().encode(message.text)
    await write_new_category(message.bot['session'], message['from']['id'], encode_category_name, expense)
    await message.answer(
        markdown.text(
            markdown.text(markdown.hitalic(AnswerEnum.DATA_RECORDED.value)),
            markdown.text(f"{AnswerEnum.CHAPTER.value}: {IncomeExpenseEnum.EXPENSE.value}"),
            markdown.text(f"{AnswerEnum.CATEGORY.value}: {message.text}"),
            sep="\n",
        ),
        parse_mode="HTML",
        reply_markup=types.ReplyKeyboardRemove(),
    )

    await state.finish()


def register_handlers_new_category(dp: Dispatcher):
    """Register command in this file."""
    dp.register_message_handler(
        add_category,
        state='*',
        commands='add_category',
    )
    dp.register_message_handler(
        enter_name_category,
        state=AddCategoryState.category,
    )
