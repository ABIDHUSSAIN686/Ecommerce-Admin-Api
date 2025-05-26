from sqlalchemy.orm import Session
from app.infrastructure.db.models.sales_model import Sale
from sqlalchemy import func

# Repository class
class SalesRepository:
    
    # Initialize the repository with a SQLAlchemy database session
    def __init__(self, db: Session):
        self.db = db

    # Calculate daily sales revenue summary
    def calculate_summary(self):
        results = self.db.query( func.date_trunc('day', Sale.sale_date).label('day'),
        func.sum(Sale.total_price).label('revenue')
        ).group_by('day').order_by('day').all()
        
        return results 
