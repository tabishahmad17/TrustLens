
from db_connection import get_audit_connection

connection = get_audit_connection()

try:
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            current_database(),
            current_user,
            current_schema(),
            has_schema_privilege(
                current_user, 'ops', 'USAGE'
            ),
            has_table_privilege(
                current_user, 'ops.audit_log', 'INSERT'
            );
    """)

    result = cursor.fetchone()

    print("Database:", result[0])
    print("Connected user:", result[1])
    print("Current schema:", result[2])
    print("Schema access:", result[3])
    print("INSERT permission:", result[4])

except Exception as error:
    print("Error:", error)

finally:
    connection.close()