import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine
from app.infrastructure.db.models.base_model import Base
from app.infrastructure.db.session import DATABASE_URL

# Function to create the database if it doesnot already exist
def create_database_if_not_exists():
    import re

    db_name = DATABASE_URL.rsplit('/', 1)[-1]
    db_url_without_db = re.sub(r"/[^/]+$", "/postgres", DATABASE_URL)

    conn = psycopg2.connect(db_url_without_db)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()

    cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
    exists = cursor.fetchone()

    if not exists:
        cursor.execute(f"CREATE DATABASE {db_name}")
        print(f"Created database: {db_name}")
    else:
        print(f"Database '{db_name}' already exists")

    cursor.close()
    conn.close()

# Function to create tables based on models defined using SQLAlchemy's Base
def create_tables():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
