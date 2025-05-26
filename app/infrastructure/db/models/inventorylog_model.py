from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.infrastructure.db.models.base_model import Base

class InventoryLog(Base):
    # Name of table in database
    __tablename__ = "inventory_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    previous_stock = Column(Integer)
    new_stock = Column(Integer)
    changed_at = Column(DateTime(timezone=True), server_default=func.now())
