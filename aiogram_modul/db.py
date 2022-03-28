import os

import sqlite3

from aiogram_modul.constants import CATEGORY_INCOME_LIST, CATEGORY_EXPENSE_LIST, USER_IDS

conn = sqlite3.connect(os.path.join("finance.db"))
cursor = conn.cursor()


def get_category_id_by_name(category_name: str) -> int:
    cursor.execute(f'SELECT id FROM category WHERE name = "{category_name}"')
    rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append(row[0])
    return result[0]


def write_budgeting(user_id: int, category_name: str, amount: float):
    category_id = get_category_id_by_name(category_name)
    sql = (f"INSERT INTO budgeting (amount, user_id, category_id) "
           f"VALUES ({amount}, {user_id}, {category_id})")
    cursor.execute(sql)
    conn.commit()


def get_cursor():
    return cursor


def _init_db():
    """Инициализирует БД"""
    with open("createdb.sql", "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def _init_insert_user():
    sql = "INSERT INTO user (telegram_id, name) VALUES (?, ?)"
    values = [(telegram_id, name) for telegram_id, name in USER_IDS.items()]
    cursor.executemany(sql, values)
    conn.commit()


def _init_insert_category():
    sql = "INSERT INTO category (name, is_expense) VALUES (?, ?)"
    values = [
        (category, False) for category in CATEGORY_INCOME_LIST
    ]
    values += [
        (category, True) for category in CATEGORY_EXPENSE_LIST
    ]
    cursor.executemany(sql, values)
    conn.commit()


def check_db_exists():
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    cursor.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table' AND name='category'")
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()
    _init_insert_user()
    _init_insert_category()


check_db_exists()
