from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from typing import Optional
from app.infrastructure.db.models.product_model import Product
from app.infrastructure.db.models.sales_model import Sale
from app.api.v1.schema.sales_schema import SaleRead, RevenueSummary, SalesComparison
from app.infrastructure.db.session import get_db

router = APIRouter()

# Request for getting the sales records
# based on the optional parameters (start_date,end_date,category) 
# passed as query parameter
@router.get("/", response_model=list[SaleRead])
def get_sales(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    product_id: Optional[int] = Query(None),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db),):
    # Fetching the sales items
    query = db.query(Sale).join(Product, Sale.product_id == Product.id)
    if start_date:
        query = query.filter(Sale.sale_date >= start_date)
    if end_date:
        query = query.filter(Sale.sale_date <= end_date)
    if product_id:
        query = query.filter(Sale.product_id == product_id)
    if category:
        query = query.filter(Product.category == category)
    
    # Returning the whole list of sale items 
    sales = query.all()

    return sales

# Request for getting aggregate total revenue by period 
# based on the optional parameters (daily, weekly, monthly, yearly)
# passed as query parameter
@router.get("/revenue_summary", response_model=list[RevenueSummary])
def revenue_summary(
    period: str = Query("daily", regex="^(daily|weekly|monthly|yearly)$"),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db),):
    """
    Aggregate total revenue by period: daily, weekly, monthly, yearly
    """
    query = db.query(Sale).join(Product, Sale.product_id == Product.id)
    # Dates validation checks
    if start_date:
        query = query.filter(Sale.sale_date >= start_date)
    if end_date:
        query = query.filter(Sale.sale_date <= end_date)
    # Provided category should exists in product table
    if category:
        query = query.filter(Product.category == category)

    if period == "daily":
        group_expr = func.date_trunc('day', Sale.sale_date)
        period_label = func.to_char(group_expr, 'YYYY-MM-DD')
    elif period == "weekly":
        group_expr = func.date_trunc('week', Sale.sale_date)
        period_label = func.to_char(group_expr, 'IYYY-IW')
    elif period == "monthly":
        group_expr = func.date_trunc('month', Sale.sale_date)
        period_label = func.to_char(group_expr, 'YYYY-MM')
    else:
        group_expr = func.date_trunc('year', Sale.sale_date)
        period_label = func.to_char(group_expr, 'YYYY')

    query = query.group_by(group_expr).order_by(group_expr)

    results = query.with_entities(period_label.label("period"), func.sum(Sale.total_price).label("total_revenue")).all()

    summaries = [
        # Tranforming the reponse of the api into RevenueSummary schema 
        RevenueSummary(period=period_, total_revenue=total) for period_, total in results
    ]

    return summaries

# Request for comparing total revenue between two date ranges, optionally filtered by category
# based on the optional parameters (period1_start, period1_end, period2_start, period2_end, category)
# passed as query parameter
@router.get("/compare_revenue", response_model=SalesComparison)
def compare_revenue(
    period1_start: datetime = Query(..., example="2024-01-01T00:00:00"),
    period1_end: datetime = Query(..., example="2024-01-31T23:59:59"),
    period2_start: datetime = Query(..., example="2025-01-01T00:00:00"),
    period2_end: datetime = Query(..., example="2025-01-31T23:59:59"),
    category: Optional[str] = Query(None, example="Electronics"),
    db: Session = Depends(get_db),):
    """
    Compare revenue between two date ranges (period1 and period2)
    
    """
    def get_revenue(start, end):
        q = db.query(func.sum(Sale.total_price))
        if category:
            q = q.join(Product, Sale.product_id == Product.id).filter(Product.category == category)
        q = q.filter(Sale.sale_date >= start, Sale.sale_date <= end)
        return q.scalar() or 0.0
    # Getting revenue for 1 period
    rev1 = get_revenue(period1_start, period1_end)
    # Getting revenue for 2 period
    rev2 = get_revenue(period2_start, period2_end)

    # Tranforming the reponse of the api into SalesComparison schema 
    return SalesComparison(period1_revenue=rev1, period2_revenue=rev2, difference=rev2 - rev1)
