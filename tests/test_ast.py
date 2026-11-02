
import sqlglot

query = """
SELECT
    CASE
        WHEN 1 = 1 THEN 1
        ELSE 0
    END
FROM raw.orders
"""

tree = sqlglot.parse_one(query, read="postgres")

print("PARSED SQL:")
print(tree)

print("\nAST NODES:")

for node in tree.walk():
    print(
        type(node).__name__,
        "| key:", node.key,
        "| SQL name:", node.sql_name()
        if hasattr(node, "sql_name") else "N/A"
    )
