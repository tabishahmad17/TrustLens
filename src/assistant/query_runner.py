
from db_connection import get_db_connection
from sql_validator import validate_sql


MAX_ROWS = 100
QUERY_TIMEOUT = "10s"


def execute_query(sql):

    # 1. Validate SQL before connecting
    is_valid, message = validate_sql(sql)

    if not is_valid:
        return {
            "success": False,
            "error": message
        }

    connection = None
    cursor = None

    try:

        # 2. Connect to PostgreSQL
        connection = get_db_connection()

        # 3. Enable read-only transaction
        connection.set_session(
            readonly=True,
            autocommit=False
        )

        cursor = connection.cursor()

        # 4. Set 10-second transaction-local timeout
        cursor.execute(
            "SELECT set_config('statement_timeout', %s, true)",
            (QUERY_TIMEOUT,)
        )

        # 5. Execute validated SQL
        cursor.execute(sql.rstrip().rstrip(";"))

        # 6. Get column names
        columns = [
            description[0]
            for description in cursor.description
        ]

        # 7. Fetch maximum 100 rows
        rows = cursor.fetchmany(MAX_ROWS)

        results = [
            dict(zip(columns, row))
            for row in rows
        ]

        return {
            "success": True,
            "columns": columns,
            "rows": results,
            "row_count": len(results)
        }

    except Exception as error:

        if connection:
            connection.rollback()

        return {
            "success": False,
            "error": str(error)
        }

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.rollback()
            connection.close()
