
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, URL, text
from dotenv import load_dotenv
import os

load_dotenv()

DATA_DIR = Path("data/raw")
CHUNK_SIZE = 50_000

FILES = {
    "olist_customers_dataset.csv": "customers",
    "olist_geolocation_dataset.csv": "geolocation",
    "olist_order_items_dataset.csv": "order_items",
    "olist_order_payments_dataset.csv": "order_payments",
    "olist_order_reviews_dataset.csv": "order_reviews",
    "olist_orders_dataset.csv": "orders",
    "olist_products_dataset.csv": "products",
    "olist_sellers_dataset.csv": "sellers",
    "product_category_name_translation.csv": "category_translation",
}

url = URL.create(
    "postgresql+psycopg2",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", "5432")),
    database=os.getenv("DB_NAME", "trustlens"),
)

engine = create_engine(url)

try:
    with engine.begin() as connection:
        connection.execute(
            text("CREATE SCHEMA IF NOT EXISTS raw")
        )

    for filename, table_name in FILES.items():
        file_path = DATA_DIR / filename

        if not file_path.exists():
            print(f"MISSING: {filename}")
            continue

        print(f"\nLoading {filename}...")

        first_chunk = True

        for chunk in pd.read_csv(
            file_path,
            chunksize=CHUNK_SIZE,
            dtype=str,
            keep_default_na=False,
            encoding="utf-8-sig",
        ):
            chunk.to_sql(
                name=table_name,
                con=engine,
                schema="raw",
                if_exists="replace" if first_chunk else "append",
                index=False,
                chunksize=10_000,
                method="multi",
            )
            first_chunk = False

        with engine.connect() as connection:
            count = connection.execute(
                text(f'SELECT COUNT(*) FROM raw."{table_name}"')
            ).scalar_one()

        print(f"SUCCESS: raw.{table_name} — {count:,} rows")

    print("\nDataset loading process finished.")

finally:
    engine.dispose()
