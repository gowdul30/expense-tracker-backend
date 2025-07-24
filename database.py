from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Replace credentials accordingly
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:tretyu654678%40M@localhost:3306/expense_db"
# Create a connection engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

# Create a DB session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()
