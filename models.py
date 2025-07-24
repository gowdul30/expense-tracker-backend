from sqlalchemy import Column, Integer, String, Float, DateTime, func
from database import Base

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String(100), nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())  # ✅ auto timestamp

