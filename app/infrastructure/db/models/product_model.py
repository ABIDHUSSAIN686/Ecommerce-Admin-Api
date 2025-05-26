from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.infrastructure.db.models.base_model import Base

class Product(Base):
    # Name of table in database
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=True)

    inventory = relationship("Inventory", back_populates="product", uselist=False)
