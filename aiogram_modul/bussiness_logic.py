"""Write entry in db."""

import sqlite3
from sqlite3 import Error


def post_sql_query(sql_query):
    """Connect with db."""
    database = 'telebot/telebot.db'
    with sqlite3.connect(database) as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(sql_query)
            connection.commit()
        except Error:
            pass
        result = cursor.fetchall()
        return result


def write_entry(name_user, income_or_expense, category_income_or_expense, amount):
    """Write entry in db."""
    write_entry_query = f'INSERT INTO budgeting (name, income_expense, category, amount) VALUES ("{name_user}", "{income_or_expense}", "{category_income_or_expense}", "{amount}");'
    post_sql_query(write_entry_query)


def check_is_digit(number):
    """Check the number if the amount that we enter."""
    try:
        amount = round(float(number), 2)
    except ValueError:
        amount = 0

    return amount
