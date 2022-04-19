from datetime import datetime
from typing import List

from sqlalchemy import extract, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from aiogram_modul.constants import CategoryIncomeEnum, CategoryExpenseList
from config import database_async_url
from database.base_model import StatisticsBase

from database.models import Base, Budgeting, Category, User


async def create_async_database():
    engine = create_async_engine(database_async_url)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    async with async_session() as session:
        return session


async def get_category_id_by_name(session: AsyncSession, category_name: str) -> int:
    categories = await session.execute(select(Category).where(Category.name == category_name))
    category = categories.scalars().first()

    return category.id


async def get_all_user_telegram_id(session: AsyncSession) -> list:
    result = await session.execute(select(User))
    return [user.telegram_id for user in result.scalars()]


async def create_new_user(session: AsyncSession, telegram_id: int, username: str, locale: str):
    default_categories = await session.execute(select(Category).where(Category.default == True))
    session.add(User(
        telegram_id=telegram_id,
        username=username,
        locale=locale,
        categories=[category for category in default_categories.scalars()],
    ))
    await session.commit()


async def get_user_by_telegram_id(session: AsyncSession, telegram_id: int):
    users = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = users.scalars().first()

    return user


async def write_budgeting(session: AsyncSession, telegramm_id: int, category_name: str, amount: float):
    category_id = await get_category_id_by_name(session, category_name)
    user = await get_user_by_telegram_id(session, telegramm_id)
    session.add(Budgeting(amount=amount, user_id=user.id, category_id=category_id))
    await session.commit()


async def write_new_category(session: AsyncSession, telegramm_id: int, category_name: str, expense: bool):
    user = await get_user_by_telegram_id(session, telegramm_id)
    session.add(Category(name=category_name, is_expense=expense, default=False, users=[user]))
    await session.commit()


async def get_categories_by_user(session: AsyncSession, telegramm_id: int, expense: bool) -> List[str]:
    user = await get_user_by_telegram_id(session, telegramm_id)
    user_categories = await session.execute(
        select(Category.name).join(Category.users).filter(User.id == user.id, Category.is_expense == expense)
    )
    return list(user_categories.scalars())


async def get_history_month(session: AsyncSession, telegramm_id: int) -> List[StatisticsBase]:
    user = await get_user_by_telegram_id(session, telegramm_id)
    current_month = datetime.now().month
    statistic_by_month = await session.execute(
        select(Category.name, Budgeting.amount, Budgeting.created_date).join(Budgeting.category).where(
            Budgeting.user_id == user.id,
            extract('month', Budgeting.created_date) == current_month),
    )
    row_result = statistic_by_month.fetchall()
    result = [
        StatisticsBase(category_name=row[0], amount=row[1], date=row[2].strftime("%d-%m-%Y"))
        for row in row_result
    ]
    return result


async def _init_insert_category(session: AsyncSession):
    list_category = [
        Category(name=category, is_expense=False, default=True)
        for category in CategoryIncomeEnum.list_value()
    ]
    list_category.extend([
        Category(name=category, is_expense=True, default=True)
        for category in CategoryExpenseList.list_value()
    ])
    session.add_all(list_category)
    await session.commit()


async def check_db_exists():
    """When new db, run this function for feel data."""
    session = await create_async_database()
    await get_statistic_month(session, 409501763)
