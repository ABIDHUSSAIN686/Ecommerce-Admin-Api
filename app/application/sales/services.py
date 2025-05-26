from sqlalchemy.orm import Session
from app.domain.sales.repository import SalesRepository

class SalesService:
     
     # Initialize the service with a database session and set up the repository
    def __init__(self, db: Session):
        self.repo = SalesRepository(db)
        
    # Retrieve the daily sales summary from the repository
    def get_summary(self):
        return self.repo.calculate_summary()
