import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(
    0,
    str(PROJECT_ROOT / "src" / "assistant")
)

from db_connection import get_audit_connection

connection = get_audit_connection()
cursor = connection.cursor()

try:
    cursor.execute("""
        INSERT INTO ops.audit_log (
            user_question,
            generated_sql,
            execution_status,
            error_message
        )
        VALUES (%s, %s, %s, %s);
    """, (
        "TrustLens audit permission test",
        "SELECT * FROM raw.orders",
        "success",
        None
    ))

    connection.commit()

    print("Audit INSERT: SUCCESS")
    print("Inserted rows:", cursor.rowcount)

except Exception as error:
    connection.rollback()
    print("Audit INSERT: FAILED")
    print("Error:", error)

finally:
    cursor.close()
    connection.close()
