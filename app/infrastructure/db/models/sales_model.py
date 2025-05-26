from sqlalchemy import Column, Integer, DateTime, ForeignKey, Float
from app.infrastructure.db.models.base_model import Base
from datetime import datetime

class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    sale_date = Column(DateTime, default=datetime)
    total_price = Column(Float)


