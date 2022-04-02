import os

from aiogram_modul.constants import CategoryIncomeEnum, CategoryExpenseList, USER_IDS
from databases import Database

database = Database(os.getenv('DATABASE_URL', 'postgres://fqwnoxoapnpriz:5b22ff1c07aadaa97cfa5b225249cff543871279ada909af47833f77b7e82058@ec2-99-80-170-190.eu-west-1.compute.amazonaws.com:5432/d42l3k9jqhgisr'))


async def get_category_id_by_name(category_name: str) -> int:
    rows = await database.fetch_all(f"SELECT id FROM category WHERE name = '{category_name}'")
    result = []
    for row in rows:
        result.append(row[0])
    return result[0]


async def write_budgeting(user_id: int, category_name: str, amount: float):
    await database.connect()
    category_id = await get_category_id_by_name(category_name)
    sql = (f"INSERT INTO budgeting (amount, user_id, category_id) "
           f"VALUES ({amount}, {user_id}, {category_id})")
    await database.execute(sql)


async def _init_insert_user():
    sql = "INSERT INTO budget_user (telegram_id, name) VALUES (:telegram_id, :name)"
    values = [{"telegram_id": telegram_id, "name": name} for telegram_id, name in USER_IDS.items()]
    await database.execute_many(sql, values)


async def _init_insert_category():
    sql = "INSERT INTO category (name, is_expense) VALUES (:name, :is_expense)"
    values = [
        {"name": category, "is_expense": False} for category in CategoryIncomeEnum.list_value()
    ]
    values += [
        {"name": category, "is_expense": True} for category in CategoryExpenseList.list_value()
    ]
    await database.execute_many(sql, values)


async def check_db_exists():
    """When new db, run this function for feel data."""
    await _init_insert_user()
    await _init_insert_category()
