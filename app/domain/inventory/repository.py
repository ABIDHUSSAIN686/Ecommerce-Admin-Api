from sqlalchemy.orm import Session
from app.infrastructure.db.models.inventory_model import Inventory
from app.infrastructure.db.models.product_model import Product

# Repository class
class InventoryRepository:
    
    # Initialize the repository with a SQLAlchemy database session
    def __init__(self, db: Session):
        self.db = db
    
    #  Overview inventory by joining product and inventory table
    def get_inventory_overview(self):
        return self.db.query(Product.name, Inventory.stock_level).join(Product).all()
