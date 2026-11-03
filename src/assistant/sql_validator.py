import sqlglot
from sqlglot import exp


# --------------------------------------------------
# APPROVED DATABASE TABLES AND VIEWS
# --------------------------------------------------

ALLOWED_TABLES = {
    ("raw", "customers"),
    ("raw", "geolocation"),
    ("raw", "order_items"),
    ("raw", "order_payments"),
    ("raw", "order_reviews"),
    ("raw", "orders"),
    ("raw", "products"),
    ("raw", "sellers"),
    ("raw", "category_translation"),
    ("analytics", "v_monthly_kpis"),
    ("analytics", "v_order_facts"),
    ("analytics", "v_seller_performance"),
}


# --------------------------------------------------
# FORBIDDEN SQL OPERATIONS
# --------------------------------------------------

FORBIDDEN_NODES = {
    "insert", "update", "delete",
    "create", "drop", "alter",
    "command", "merge", "grant",
    "revoke", "transaction", "copy",
    "set", "truncate", "into", "lock",
}


# --------------------------------------------------
# FORBIDDEN POSTGRESQL FUNCTIONS
# --------------------------------------------------

FORBIDDEN_FUNCTIONS = {
    "PG_SLEEP", "PG_READ_FILE", "PG_READ_BINARY_FILE",
    "PG_LS_DIR", "LO_IMPORT", "LO_EXPORT", "DBLINK",
    "DBLINK_EXEC", "SET_CONFIG", "PG_TERMINATE_BACKEND",
    "PG_CANCEL_BACKEND", "PG_ADVISORY_LOCK",
    "PG_ADVISORY_XACT_LOCK", "NEXTVAL", "SETVAL", "PG_NOTIFY",
}


# --------------------------------------------------
# APPROVED ANALYTICAL FUNCTIONS AND BOOLEAN OPERATORS
# --------------------------------------------------

ALLOWED_FUNCTIONS = {
    "COUNT", "SUM", "AVG", "MIN", "MAX",
    "ROUND", "ABS", "CEIL", "CEILING", "FLOOR", "POWER", "SQRT",
    "COALESCE", "NULLIF", "GREATEST", "LEAST",
    "LOWER", "UPPER", "TRIM", "BTRIM", "LENGTH", "CHAR_LENGTH",
    "SUBSTRING", "REPLACE", "CONCAT",
    "DATE_TRUNC", "TIMESTAMP_TRUNC", "DATE_PART", "EXTRACT", "AGE", "NOW",
    "CURRENT_DATE", "CURRENT_TIMESTAMP",
    "TO_CHAR", "TO_DATE", "TO_NUMBER", "TIME_TO_STR",
    "PERCENTILE_CONT", "PERCENTILE_DISC",
    "ROW_NUMBER", "RANK", "DENSE_RANK", "LAG", "LEAD",
    "FIRST_VALUE", "LAST_VALUE", "GENERATE_SERIES",
    # SQLGlot may represent boolean operators as function nodes.
    "AND", "OR", "NOT",
}


def validate_sql(sql):
    try:
        if not sql or not sql.strip():
            return False, "SQL query cannot be empty."

        statements = sqlglot.parse(sql, read="postgres")
        if not statements or len(statements) != 1:
            return False, "Only one SQL statement is allowed."

        tree = statements[0]
        if not isinstance(tree, exp.Select):
            return False, "Only SELECT queries are allowed."

        cte_names = {
            cte.alias_or_name.lower()
            for cte in tree.find_all(exp.CTE)
        }

        for node in tree.walk():
            node_type = node.key.lower()
            if node_type in FORBIDDEN_NODES:
                return False, f"SQL operation not allowed: {node_type}"

            if isinstance(node, exp.Table):
                table_name = node.name.lower()
                schema_name = node.db.lower() if node.db else ""

                if not schema_name and table_name in cte_names:
                    continue

                if not schema_name:
                    return False, f"Table must use an approved schema: {table_name}"

                if node.catalog:
                    return False, "Cross-database queries are not allowed."

                if (schema_name, table_name) not in ALLOWED_TABLES:
                    return False, f"Table not allowed: {schema_name}.{table_name}"

            # Boolean operators are SQL syntax nodes, not callable functions.
            if isinstance(node, (exp.And, exp.Or, exp.Not)):
                continue

            if isinstance(node, (exp.Case, exp.If, exp.Star, exp.Cast)):
                continue

            if isinstance(node, exp.Func):
                if isinstance(node, exp.Anonymous):
                    function_name = node.name.upper()
                else:
                    function_name = node.sql_name().upper()

                if isinstance(node, exp.Anonymous) and "." in function_name:
                    return False, "Schema-qualified function calls are not allowed."

                if function_name in FORBIDDEN_FUNCTIONS:
                    return False, f"Function not allowed: {function_name}"

                if function_name not in ALLOWED_FUNCTIONS:
                    return False, f"Function not approved: {function_name}"

        return True, "SQL validation successful."

    except Exception as error:
        return False, f"Invalid SQL: {error}"
