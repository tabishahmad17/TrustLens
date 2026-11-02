import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

# Load .env from TrustLens project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


def create_connection(user, password):

    try:
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=user,
            password=password,
            connect_timeout=10
        )

        return connection

    except psycopg2.Error as error:
        raise RuntimeError(
            f"PostgreSQL connection failed: {error}"
        ) from error


def get_db_connection():
    """Read-only connection for SQL query execution."""

    return create_connection(
        os.getenv("DB_READER_USER"),
        os.getenv("DB_READER_PASSWORD")
    )


def get_audit_connection():
    """Separate connection for audit logging."""

    return create_connection(
        os.getenv("DB_AUDIT_USER"),
        os.getenv("DB_AUDIT_PASSWORD")
    )
def get_admin_connection():
    """Administrator connection for database setup."""

    return create_connection(
        os.getenv("DB_USER"),
        os.getenv("DB_PASSWORD")
    )