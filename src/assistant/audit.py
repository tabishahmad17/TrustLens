
from db_connection import (
    get_admin_connection,
    get_audit_connection
)


def create_audit_table():

    connection = None
    cursor = None

    try:
        # Admin account: database setup only
        connection = get_admin_connection()
        cursor = connection.cursor()

        cursor.execute("""
            CREATE SCHEMA IF NOT EXISTS ops;

            CREATE TABLE IF NOT EXISTS ops.audit_log (
                id BIGSERIAL PRIMARY KEY,
                user_question TEXT NOT NULL,
                generated_sql TEXT,
                execution_status VARCHAR(30) NOT NULL,
                error_message TEXT,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
            );
        """)

        connection.commit()
        print("Audit table created successfully!")

    except Exception:
        if connection:
            connection.rollback()
        raise

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


def log_interaction(
    question,
    generated_sql,
    status,
    error_message=None
):

    connection = None
    cursor = None

    try:
        # Audit account: INSERT only
        connection = get_audit_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO ops.audit_log (
                user_question,
                generated_sql,
                execution_status,
                error_message
            )
            VALUES (%s, %s, %s, %s);
        """, (
            question,
            generated_sql,
            status,
            error_message
        ))

        connection.commit()
        print("Interaction logged successfully!")

    except Exception:
        if connection:
            connection.rollback()
        raise

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()
