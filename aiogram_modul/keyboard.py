"""Keyboard for bot."""

from aiogram.types import ReplyKeyboardMarkup

from aiogram_modul.constants import (
    BackEnum,
    IncomeExpenseEnum,
    HistoryChoiceEnum,
    StatisticsChoiceEnum,
    StatisticsChoiceMonthEnum,
)

income_and_expense_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
).add(*IncomeExpenseEnum.list_value()).row(BackEnum.BACK.value)

choice_variant_statistics = ReplyKeyboardMarkup(
    resize_keyboard=True,
).add(*StatisticsChoiceEnum.list_value()).row(BackEnum.BACK.value)

choice_variant_month_statistics = ReplyKeyboardMarkup(
    resize_keyboard=True,
).add(*StatisticsChoiceMonthEnum.list_value_name_month()).row(BackEnum.BACK.value)

choice_variant_history = ReplyKeyboardMarkup(
    resize_keyboard=True,
).add(*HistoryChoiceEnum.list_value()).row(BackEnum.BACK.value)

back_keyboard_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
).row(BackEnum.BACK.value)
