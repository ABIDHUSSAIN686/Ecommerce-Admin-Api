from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

# Read the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency function to provide a new DB session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
