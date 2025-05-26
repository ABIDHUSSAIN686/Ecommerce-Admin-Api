from sqlalchemy.orm import Session
from app.domain.inventory.repository import InventoryRepository

# Service class
class InventoryService:
     
     # Initialize the service with a database session and set up the repository
    def __init__(self, db: Session):
        self.repo = InventoryRepository(db)

    # Retrieving the inventory data from repository   
    def get_status(self):
        return self.repo.get_inventory_overview()
