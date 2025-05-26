from pydantic import BaseModel

# Schemas for transforming request response  
class ProductStock(BaseModel):
    id: int
    name: str
    stock_level: int

    class Config:
        from_attributes = True