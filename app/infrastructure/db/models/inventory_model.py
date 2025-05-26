from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.infrastructure.db.models.base_model import Base

class Inventory(Base):
    # Name of table in database
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    stock_level = Column(Integer)

    product = relationship("Product", back_populates="inventory")
