from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from groqAI import router as ask_ai_router  # Import the router from ask-ai.py

import models, schemas, crud
from database import SessionLocal, engine

# Create tables if they don't exist
models.Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI()
app.include_router(ask_ai_router)  # Include the AI router

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
def read_expenses(db: Session = Depends(get_db)):
    """
    Returns all expenses from the DB.
    """
    return crud.get_expenses(db)

@app.post("/expenses/", response_model=schemas.Expense)
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    """
    Adds a new expense to the DB.
    """
    return crud.create_expense(db, expense)
