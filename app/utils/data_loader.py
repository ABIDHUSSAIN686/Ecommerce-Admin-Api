import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.infrastructure.db.models.product_model import Product
from app.infrastructure.db.models.inventory_model import Inventory
from app.infrastructure.db.models.sales_model import Sale
from app.infrastructure.db.models.inventorylog_model import InventoryLog

PRODUCTS = [
    {"name": "Apple iPhone 15", "category": "Electronics"},
    {"name": "Samsung Galaxy S24", "category": "Electronics"},
    {"name": "HP Pavilion Laptop", "category": "Computers"},
    {"name": "Dyson V15 Vacuum", "category": "Home Appliances"},
    {"name": "LEGO Star Wars Set", "category": "Toys"},
    {"name": "Adidas Running Shoes", "category": "Footwear"},
    {"name": "Sony WH-1000XM5", "category": "Electronics"},
    {"name": "Nintendo Switch", "category": "Gaming"},
]

def seed_demo_data(db: Session):
    print("Clearing existing data...")
    db.query(InventoryLog).delete()
    db.query(Sale).delete()
    db.query(Inventory).delete()
    db.query(Product).delete()
    db.commit()

    print("Inserting demo products...")
    product_objs = []
    for prod in PRODUCTS:
        product = Product(name=prod["name"], category=prod["category"])
        db.add(product)
        product_objs.append(product)
    db.commit()

    print("Seeding inventory...")
    for product in product_objs:
        inventory = Inventory(product_id=product.id, stock_level=random.randint(10, 100))
        db.add(inventory)
    db.commit()

    print("Generating simulated sales...")
    for _ in range(300):
        product = random.choice(product_objs)
        quantity = random.randint(1, 5)
        price_per_unit = random.uniform(20.0, 800.0)
        total_price = round(price_per_unit * quantity, 2)
        days_ago = random.randint(1, 90)
        sale_date = datetime.now() - timedelta(days=days_ago)

        sale = Sale(
            product_id=product.id,
            quantity=quantity,
            sale_date=sale_date,
            total_price=total_price
        )
        db.add(sale)

    db.commit()
    print("Demo data seeded successfully.")
