from sqlalchemy import Column, Integer, String, Float
from database import Base


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(100))

    amount = Column(Float)

    category = Column(String(100))