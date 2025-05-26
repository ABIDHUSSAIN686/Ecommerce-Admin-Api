from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from fastapi import APIRouter, Depends, Body, Query, HTTPException
from typing import Optional
from app.infrastructure.db.models.product_model import Product
from app.infrastructure.db.models.inventory_model import Inventory
from app.infrastructure.db.models.inventorylog_model import  InventoryLog
from app.api.v1.schema.product_schema import ProductStock
from app.api.v1.schema.inventory_schema import InventoryLogEntry
from app.api.v1.schema.inventory_schema import InventoryStatus
from app.infrastructure.db.session import get_db
from app.api.v1.schema.sales_schema import InventoryUpdate

# Creating the APIRouter object 
api_router = APIRouter()

# Request for getting the status of the inventory 
# based on the threshold 
# passed as query parameter
@api_router.get("/status", response_model=list[InventoryStatus])
def get_inventory_status( low_stock_threshold: Optional[int] = Query(None), db: Session = Depends(get_db),):
    # Fetching the inventory items and repective products details 
    query = db.query(Inventory).options(joinedload(Inventory.product))
    # If threshold is not null. Extract all inventory from system 
    if low_stock_threshold is not None:
        query = query.filter(Inventory.stock_level <= low_stock_threshold)
    
    # Returning the whole list of inventory 
    inventories = query.all()

    return [
        # Tranforming the reponse of the api into InventoryStatus schema 
        InventoryStatus( id=inv.id, name=inv.product.name, stock_level=inv.stock_level)
        for inv in inventories
    ]

# Request for updating the inventory using the product_id and stock_level 
# based on the threshold 
# passed as query parameter
@api_router.put("/update", response_model=InventoryStatus)
def update_inventory(update: InventoryUpdate = Body(...),db: Session = Depends(get_db),):
    inv = db.query(Inventory).options(joinedload(Inventory.product))\
        .filter(Inventory.product_id == update.product_id).first()

    #  If product_id is invalid throw 404(NOT FOUND)
    if not inv:
        raise HTTPException(status_code=404, detail="Inventory not found for product")

    previous = inv.stock_level
    # Updating the existing stock level
    inv.stock_level = update.stock_level
    # If the stock_level is updated. Add the log against that product for tracking the inventory change
    db.add(InventoryLog(product_id=update.product_id, previous_stock=previous, new_stock=update.stock_level,))
    # Sucessfully committed
    db.commit()
    db.refresh(inv)
    # Tranforming the reponse of the api into required payload
    return { "id": inv.id, "name": inv.product.name, "stock_level": inv.stock_level,}

# Request for getting the inventory change logs against product_id
# based on the product_id 
# passed as query parameter
@api_router.get("/logs", response_model=list[InventoryLogEntry])
def get_inventory_logs( product_id: int = Query(..., description="Filter logs by product ID"), db: Session = Depends(get_db)):
    # Filtering inventory data based on product_id
    # Order by changed_at
    logs = db.query(InventoryLog)\
        .filter(InventoryLog.product_id == product_id)\
        .order_by(InventoryLog.changed_at.desc())\
        .all()
    
    return logs