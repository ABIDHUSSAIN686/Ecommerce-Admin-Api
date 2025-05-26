from pydantic import BaseModel
from datetime import datetime

# Schemas for transforming request response  
class InventoryStatus(BaseModel):
    id: int
    name: str
    stock_level: int

    class Config:
        orm_mode = True

class InventoryLogEntry(BaseModel):
    id: int
    product_id: int
    previous_stock: int
    new_stock: int
    changed_at: datetime

    class Config:
        orm_mode = True 