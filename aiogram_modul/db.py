import os

import asyncio

from aiogram_modul.constants import CATEGORY_INCOME_LIST, CATEGORY_EXPENSE_LIST, USER_IDS
from databases import Database

database = Database(os.getenv('DATABASE_URL', 'postgres://fqwnoxoapnpriz:5b22ff1c07aadaa97cfa5b225249cff543871279ada909af47833f77b7e82058@ec2-99-80-170-190.eu-west-1.compute.amazonaws.com:5432/d42l3k9jqhgisr'))


async def get_category_id_by_name(category_name: str) -> int:
    rows = await database.fetch_all(f"SELECT id FROM category WHERE name = '{category_name}'")
    result = []
    for row in rows:
        result.append(row[0])
    return result[0]


async def write_budgeting(user_id: int, category_name: str, amount: float):
    category_id = await get_category_id_by_name(category_name)
    sql = (f"INSERT INTO budgeting (amount, user_id, category_id) "
           f"VALUES ({amount}, {user_id}, {category_id})")
    await database.execute(sql)


# async def _init_db():
#     """Инициализирует БД"""
#     async with open("createdb.sql", "r") as f:
#         sqls = await f.read()
#     await asyncio.gather(*(database.execute(sql) for sql in sqls.split(';')))
#

async def _init_insert_user():
    sql = "INSERT INTO budget_user (telegram_id, name) VALUES (:telegram_id, :name)"
    values = [{"telegram_id": telegram_id, "name": name} for telegram_id, name in USER_IDS.items()]
    await database.execute_many(sql, values)


async def _init_insert_category():
    sql = "INSERT INTO category (name, is_expense) VALUES (:name, :is_expense)"
    values = [
        {"name": category, "is_expense": False} for category in CATEGORY_INCOME_LIST
    ]
    values += [
        {"name": category, "is_expense": True} for category in CATEGORY_EXPENSE_LIST
    ]
    await database.execute_many(sql, values)
#
#
# async def check_db_exists():
#     """Проверяет, инициализирована ли БД, если нет — инициализирует"""
#     # table_exists = await database.fetch_all(
#     #     "SELECT id FROM budgeting"
#     # )
#     # if table_exists:
#     #     return
#     await _init_insert_user()
#     await _init_insert_category()
