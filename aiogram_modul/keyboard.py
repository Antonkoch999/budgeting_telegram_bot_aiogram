"""Keyboard for bot."""

from aiogram.types import ReplyKeyboardMarkup

user_key_board_list = ['Кристина', 'Антон']
income_and_expense_list = ['Доход', 'Расход']
category_income_list = ['Зарплата', 'ИП', 'Hermes', 'Другое']
category_expense_list = ['Машина', 'Лечение', 'Продукты', 'Fast-Food', 'Кредиты', 'Хоз.нужды',
                         'Коммунальные услуги, связь', 'Досуг']

user_key_board = ReplyKeyboardMarkup(resize_keyboard=True).add(*user_key_board_list).row('Отмена')
income_and_expense = ReplyKeyboardMarkup(resize_keyboard=True).add(*income_and_expense_list).row('Назад')
category_income = ReplyKeyboardMarkup(resize_keyboard=True).add(*category_income_list).row('Назад')
category_expense = ReplyKeyboardMarkup(resize_keyboard=True).add(*category_expense_list).row('Назад')
