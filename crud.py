from sqlalchemy.orm import Session
import models, schemas

# Get all expenses
def get_expenses(db: Session):
    return db.query(models.Expense).all()

# Create a new expense
def create_expense(db: Session, expense: schemas.ExpenseCreate):
    db_expense = models.Expense(**expense.dict())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense
