from app.utils.data_loader import seed_demo_data
from app.infrastructure.db.session import SessionLocal
from app.infrastructure.db.init_db import create_database_if_not_exists, create_tables

def main():
    create_database_if_not_exists()
    create_tables()

    db = SessionLocal()
    try:
        seed_demo_data(db)
    finally:
        db.close()

if __name__ == "__main__":
    main()
