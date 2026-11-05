import sqlite3

import pandas as pd

from src.etl import run_etl


def test_revenue_column_exists_and_non_negative(tmp_path):
    raw_path = tmp_path / "raw" / "orders.csv"
    processed_path = tmp_path / "processed" / "orders_clean.csv"
    database_path = tmp_path / "db" / "orders.db"

    cleaned = run_etl(raw_path, processed_path, database_path)

    assert len(cleaned) == 30
    assert "revenue" in cleaned.columns
    assert (cleaned["revenue"] >= 0).all()
    assert processed_path.exists()
    with sqlite3.connect(database_path) as connection:
        loaded = pd.read_sql_query("SELECT * FROM orders_clean", connection)
    pd.testing.assert_frame_equal(loaded, cleaned, check_dtype=False)


def test_missing_quantity_filled_with_one(tmp_path):
    raw_path = tmp_path / "raw" / "orders.csv"
    raw_path.parent.mkdir(parents=True)
    pd.DataFrame(
        [
            {
                "order_id": 1,
                "order_date": "2024-01-01",
                "product": "Coffee",
                "quantity": None,
                "unit_price": 4.5,
            }
        ]
    ).to_csv(raw_path, index=False)
    processed_path = tmp_path / "processed" / "orders_clean.csv"
    database_path = tmp_path / "db" / "orders.db"

    cleaned = run_etl(raw_path, processed_path, database_path)

    assert cleaned.loc[0, "quantity"] == 1
    assert cleaned.loc[0, "revenue"] == 4.5
    assert pd.read_csv(processed_path).loc[0, "quantity"] == 1
