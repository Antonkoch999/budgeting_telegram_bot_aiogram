import os
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from aiogram_modul.constants import CategoryIncomeEnum, CategoryExpenseList

from database.models import Base, Budgeting, Category, User


async def create_async_database():
    engine = create_async_engine(
        os.getenv('DATABASE_URL', "postgresql+asyncpg://fqwnoxoapnpriz:5b22ff1c07aadaa97cfa5b225249cff543871279ada909af47833f77b7e82058@ec2-99-80-170-190.eu-west-1.compute.amazonaws.com:5432/d42l3k9jqhgisr"),
    )

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
    session.add(User(telegram_id=telegram_id, username=username, locale=locale))
    await session.commit()


async def get_user_by_telegram_id(session: AsyncSession, telegram_id: int):
    users = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = users.scalars().first()

    return user.id


async def write_budgeting(session: AsyncSession, telegramm_id: int, category_name: str, amount: float):
    category_id = await get_category_id_by_name(session, category_name)
    user_id = await get_user_by_telegram_id(session, telegramm_id)
    session.add(Budgeting(amount=amount, user_id=user_id, category_id=category_id))
    await session.commit()


async def get_statistic_month(user_id: int = None):
    current_month = datetime.now().month


async def _init_insert_category(session: AsyncSession):
    list_category = [
        Category(name=category, is_expense=False)
        for category in CategoryIncomeEnum.list_value()
    ]
    list_category.extend([
        Category(name=category, is_expense=True)
        for category in CategoryExpenseList.list_value()
    ])
    session.add_all(list_category)
    await session.commit()


async def check_db_exists():
    """When new db, run this function for feel data."""
    session = await create_async_database()
    await _init_insert_category(session)
