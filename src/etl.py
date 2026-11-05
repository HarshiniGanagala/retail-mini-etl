"""A small retail orders ETL pipeline using pandas and SQLite."""

import sqlite3
from datetime import date, timedelta
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_ORDERS_PATH = PROJECT_ROOT / "data" / "raw" / "orders.csv"
PROCESSED_ORDERS_PATH = PROJECT_ROOT / "data" / "processed" / "orders_clean.csv"
DATABASE_PATH = PROJECT_ROOT / "db" / "orders.db"


def create_sample_orders(output_path: Path) -> None:
    """Create 30 predictable example orders, including missing quantities."""
    products = ["Coffee", "Tea", "Mug", "Notebook", "Pen"]
    quantities = [2, 1, 3, 2, None, 4, 1, 2, 3, 1, 2, 4, None, 1, 3]
    orders = [
        {
            "order_id": order_id,
            "order_date": (date(2024, 1, 1) + timedelta(days=order_id - 1)).isoformat(),
            "product": products[(order_id - 1) % len(products)],
            "quantity": quantities[(order_id - 1) % len(quantities)],
            "unit_price": [4.5, 3.25, 8.0, 5.75, 1.5][
                (order_id - 1) % len(products)
            ],
        }
        for order_id in range(1, 31)
    ]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(orders).to_csv(output_path, index=False)


def transform_orders(orders: pd.DataFrame) -> pd.DataFrame:
    """Fill missing quantities, set numeric types, and calculate revenue."""
    cleaned = orders.copy()
    cleaned["quantity"] = cleaned["quantity"].fillna(1).astype(int)
    cleaned["unit_price"] = cleaned["unit_price"].astype(float)
    cleaned["revenue"] = cleaned["quantity"] * cleaned["unit_price"]
    return cleaned


def run_etl(
    raw_path: Path = RAW_ORDERS_PATH,
    processed_path: Path = PROCESSED_ORDERS_PATH,
    database_path: Path = DATABASE_PATH,
) -> pd.DataFrame:
    """Create, transform, and load orders, then print the requested KPIs."""
    if not raw_path.exists():
        create_sample_orders(raw_path)

    orders = pd.read_csv(raw_path)
    cleaned = transform_orders(orders)

    processed_path.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(processed_path, index=False)

    database_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(database_path) as connection:
        cleaned.to_sql("orders_clean", connection, if_exists="replace", index=False)

    revenue_by_product = cleaned.groupby("product")["revenue"].sum()
    top_product = revenue_by_product.idxmax() if not revenue_by_product.empty else "None"
    print(f"total_orders: {len(cleaned)}")
    print(f"total_revenue: {cleaned['revenue'].sum()}")
    print(f"top_product_by_revenue: {top_product}")

    return cleaned


if __name__ == "__main__":
    run_etl()
