from pydantic import BaseModel


class StatisticsBase(BaseModel):
    category_name: str
    amount: float
    date: str
