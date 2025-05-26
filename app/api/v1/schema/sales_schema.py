from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

# Schemas for transforming request response  
class SaleBase(BaseModel):
    product_id: int
    quantity: int
    sale_date: datetime
    total_price: float

class SaleCreate(SaleBase):
    pass

class SaleRead(SaleBase):
    id: int
    class Config:
        orm_mode = True


class ProductRead(BaseModel):
    id: int
    name: str
    category: str
    class Config:
        orm_mode = True


class InventoryRead(BaseModel):
    product_id: int
    stock_level: int
    class Config:
        orm_mode = True


class InventoryUpdate(BaseModel):
    product_id: int
    stock_level: int


class RevenueSummary(BaseModel):
    period: str
    total_revenue: float


class SalesComparison(BaseModel):
    period1_revenue: float
    period2_revenue: float
    difference: float
