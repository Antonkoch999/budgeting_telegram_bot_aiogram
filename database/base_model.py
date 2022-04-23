from pydantic import BaseModel


class StatisticsBase(BaseModel):
    category_name: str = None
    amount: float = None
    date: str = None
