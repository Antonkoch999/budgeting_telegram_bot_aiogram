"""Keyboard for bot."""

from aiogram.types import ReplyKeyboardMarkup

from aiogram_modul.constants import (
    CATEGORY_EXPENSE_LIST,
    CATEGORY_INCOME_LIST,
    INCOME_AND_EXPENSE_LIST,
    TEXT_FOR_BUTTON_BACK,
    TEXT_FOR_BUTTON_CANCEL,
    USER_IDS,
)

user_key_board = ReplyKeyboardMarkup(
    resize_keyboard=True,
).add(*USER_IDS.values()).row(TEXT_FOR_BUTTON_CANCEL)

income_and_expense = ReplyKeyboardMarkup(
    resize_keyboard=True,
).add(*INCOME_AND_EXPENSE_LIST).row(TEXT_FOR_BUTTON_BACK)

category_income = ReplyKeyboardMarkup(
    resize_keyboard=True,
).add(*CATEGORY_INCOME_LIST).row(TEXT_FOR_BUTTON_BACK)

category_expense = ReplyKeyboardMarkup(
    resize_keyboard=True,
).add(*CATEGORY_EXPENSE_LIST).row(TEXT_FOR_BUTTON_BACK)

back_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
).row(TEXT_FOR_BUTTON_BACK)
