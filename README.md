# E-commerce Admin API

A robust backend API for managing products, inventory, and sales insights in an e-commerce system. Built with FastAPI and SQLAlchemy, following industry best practices for scalability and maintainability.

---

## Features

- Inventory tracking and updates
- Inventory change logs for audit trails
- Sales insights and analytics
- Filtering inventory by stock levels
- Environment-based configuration

---

## Tech Stack

- **FastAPI** — Modern, fast (high-performance) web framework for building APIs with Python 3.11+
- **SQLAlchemy ORM** — Database toolkit and ORM for Python
- **PostgreSQL** — Relational database system
- **Uvicorn** — ASGI server for running FastAPI applications

---

## Setup & Installation

### Prerequisites

- Python 3.11 or newer
- PostgreSQL database instance

### Installation Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/ABIDHUSSAIN686/ecommerce-admin-api.git
    cd ecommerce-admin-api
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the project root and add your database URL:
    ```env
    DATABASE_URL=postgresql://user:password@localhost:5432/dbname
    ```

5. Run database migrations (if applicable) and seed initial data:

    ```bash
    python import_script.py
    ```
    All data has been sucessfully imported into your system.

6. Start the application:
    ```bash
    uvicorn app.main:app --reload
    ```

---

## API Endpoints Overview

| Method | Endpoint                     | Description                                      |
|--------|------------------------------|------------------------------------------------|
| GET    | `/api/v1/sales/`             | Retrieve sales records with optional filters: start_date, end_date, product_id, category |
| GET    | `/api/v1/sales/revenue_summary` | Aggregate total revenue by period (daily, weekly, monthly, yearly) with optional filters |
| GET    | `/api/v1/sales/compare_revenue` | Compare total revenue between two date ranges, optionally filtered by category |
| GET    | `/api/v1/inventory/status`   | Retrieve inventory status; filter by low stock threshold |
| PUT    | `/api/v1/inventory/update`   | Update inventory stock level for a product; logs the change |
| GET    | `/api/v1/inventory/logs`     | Get inventory change logs filtered by product ID, ordered by most recent changes |

---

## Environment Variables

| Variable       | Description                  |
|----------------|------------------------------|
| `DATABASE_URL` | Database connection string (PostgreSQL) |


---


## API DOCS

Access API docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
