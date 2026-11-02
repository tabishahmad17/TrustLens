from query_runner import execute_query

sql = """
SELECT
    order_status,
    COUNT(*) AS total_orders
FROM raw.orders
GROUP BY order_status
ORDER BY total_orders DESC;
"""

result = execute_query(sql)

if result["success"]:
    print("Query executed successfully!")
    print("Rows:", result["row_count"])

    for row in result["rows"]:
        print(row)
else:
    print("Query failed:", result["error"])