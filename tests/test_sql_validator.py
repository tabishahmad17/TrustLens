
from sql_validator import validate_sql

tests = [
    "SELECT * FROM raw.orders",
    "SELECT * FROM analytics.v_monthly_kpis",
    "DELETE FROM raw.orders",
    "SELECT * FROM raw.unauthorized_table",
    "SELECT * FROM orders"
]

for query in tests:
    valid, message = validate_sql(query)

    print("\nQuery:", query)
    print("Valid:", valid)
    print("Message:", message)
