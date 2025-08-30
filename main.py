from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from auth import router as auth_router, get_current_user


from groqAI import router as ask_ai_router  # Import the router from ask-ai.py


import models, schemas, crud
from database import SessionLocal, engine



# Create tables if they don't exist
models.Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI()
app.include_router(ask_ai_router)  # Include the AI router
app.include_router(auth_router)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency: get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/expenses/", response_model=list[schemas.Expense])
def read_expenses(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.Expense).filter(models.Expense.user_id == current_user.id).all()

@app.post("/expenses/", response_model=schemas.Expense)
def create_expense(
    expense: schemas.ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_expense = models.Expense(**expense.dict(), user_id=current_user.id)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense