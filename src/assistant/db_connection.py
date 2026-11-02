import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

# Load local .env during development. Streamlit Cloud uses st.secrets.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


def get_setting(name, default=None):
    """Read a setting from environment variables or Streamlit secrets."""
    value = os.getenv(name)
    if value:
        return value

    try:
        import streamlit as st
        return st.secrets[name]
    except Exception:
        return default


def create_connection(user, password):
    """Create a TLS-protected PostgreSQL connection."""
    required = {
        "DB_HOST": get_setting("DB_HOST"),
        "DB_NAME": get_setting("DB_NAME"),
        "database username": user,
        "database password": password,
    }
    missing = [key for key, value in required.items() if not value]
    if missing:
        raise RuntimeError(
            "Missing database configuration: " + ", ".join(missing)
        )

    try:
        return psycopg2.connect(
            host=get_setting("DB_HOST"),
            port=get_setting("DB_PORT", "5432"),
            database=get_setting("DB_NAME"),
            user=user,
            password=password,
            sslmode=get_setting("DB_SSLMODE", "require"),
            connect_timeout=10,
        )
    except psycopg2.Error as error:
        raise RuntimeError(
            f"PostgreSQL connection failed: {error}"
        ) from error


def get_db_connection():
    """Read-only connection for SQL query execution."""
    return create_connection(
        get_setting("DB_READER_USER"),
        get_setting("DB_READER_PASSWORD"),
    )


def get_audit_connection():
    """Separate connection for audit logging."""
    return create_connection(
        get_setting("DB_AUDIT_USER"),
        get_setting("DB_AUDIT_PASSWORD"),
    )


def get_admin_connection():
    """Administrator connection for database setup only."""
    return create_connection(
        get_setting("DB_USER"),
        get_setting("DB_PASSWORD"),
    )
