
import os

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, text

load_dotenv()

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
    with engine.connect() as connection:

        print("TRUSTLENS DATA QUALITY REPORT")
        print("=" * 45)

        # 1. Check raw table row counts
        tables = [
            "customers",
            "geolocation",
            "order_items",
            "order_payments",
            "order_reviews",
            "orders",
            "products",
            "sellers",
            "category_translation",
        ]

        print("\n1. RAW TABLE ROW COUNTS")
        print("-" * 45)

        for table in tables:
            count = connection.execute(
                text(f'SELECT COUNT(*) FROM raw."{table}"')
            ).scalar_one()

            print(f"{table:<25} {count:>10,} rows")

        # 2. Check order IDs
        print("\n2. ORDER ID QUALITY")
        print("-" * 45)

        order_quality = connection.execute(
            text("""
                SELECT
                    COUNT(*) AS total_rows,
                    COUNT(order_id) AS non_missing_ids,
                    COUNT(DISTINCT order_id) AS unique_ids
                FROM raw.orders
            """)
        ).mappings().one()

        total_rows = order_quality["total_rows"]
        non_missing_ids = order_quality["non_missing_ids"]
        unique_ids = order_quality["unique_ids"]

        duplicate_ids = non_missing_ids - unique_ids
        missing_ids = total_rows - non_missing_ids

        print(f"Total orders:       {total_rows:,}")
        print(f"Non-missing IDs:    {non_missing_ids:,}")
        print(f"Unique order IDs:   {unique_ids:,}")

        # 3. Check delivery dates
        print("\n3. DELIVERY DATE QUALITY")
        print("-" * 45)

        date_quality = connection.execute(
            text("""
                SELECT
                    COUNT(*) FILTER (
                        WHERE order_delivered_customer_date = ''
                    ) AS missing_actual_dates,
                    COUNT(*) FILTER (
                        WHERE order_estimated_delivery_date = ''
                    ) AS missing_estimated_dates
                FROM raw.orders
            """)
        ).mappings().one()

        print(
            "Missing actual delivery dates:   "
            f"{date_quality['missing_actual_dates']:,}"
        )
        print(
            "Missing estimated delivery dates: "
            f"{date_quality['missing_estimated_dates']:,}"
        )

        # 4. Show validation status
        print("\n4. VALIDATION STATUS")
        print("-" * 45)

        if duplicate_ids == 0 and missing_ids == 0:
            print("PASS: Order IDs are present and unique.")
        else:
            print("FAIL: Missing or duplicate order IDs found.")

        if date_quality["missing_estimated_dates"] == 0:
            print("PASS: Estimated delivery dates are complete.")
        else:
            print("WARNING: Some estimated delivery dates are missing.")

        # 5. Check delivered orders with missing actual dates
        print("\n5. DELIVERED ORDERS WITH MISSING DATES")
        print("-" * 45)

        missing_delivered_dates = connection.execute(
            text("""
                SELECT COUNT(*)
                FROM raw.orders
                WHERE order_status = 'delivered'
                  AND order_delivered_customer_date = ''
            """)
        ).scalar_one()

        print(
            "Delivered orders missing actual dates: "
            f"{missing_delivered_dates:,}"
        )

        if missing_delivered_dates > 0:
            print(f"WARNING: Review {missing_delivered_dates} records.")
            print(
                "ACTION: Investigate these records "
                "before delivery analysis."
            )
        else:
            print("PASS: All delivered orders have actual dates.")

        print("\nValidation report completed.")

finally:
    engine.dispose()
