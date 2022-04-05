import datetime

from sqlalchemy import Column, Integer, String, Table, ForeignKey, Boolean, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


user_category = Table(
    'user_category',
    Base.metadata,
    Column('user_id', ForeignKey('User.id')),
    Column('category_id', ForeignKey('Category.id'))
)


class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True, autoincrement=True)

    budgets = relationship("Budgeting", back_populates="user")
    categories = relationship("Category", secondary=user_category, back_populates="users")

    telegram_id = Column(Integer, unique=True)
    username = Column(String(255))
    locale = Column(String(255))


class Category(Base):
    __tablename__ = 'Category'

    id = Column(Integer, primary_key=True, autoincrement=True)

    users = relationship("User", secondary=user_category, back_populates="categories")
    budgets = relationship("Budgeting", back_populates="category")

    name = Column(String(255))
    is_expense = Column(Boolean)


class Budgeting(Base):
    __tablename__ = 'Budgeting'

    id = Column(Integer, primary_key=True, autoincrement=True)

    category_id = Column(Integer, ForeignKey('Category.id'))
    category = relationship("Category", back_populates="budgets")
    user_id = Column(Integer, ForeignKey('User.id'))
    user = relationship("User", back_populates="budgets")

    amount = Column(Float)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
