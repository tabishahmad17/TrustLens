
from db_connection import get_db_connection

try:
    connection = get_db_connection()

    cursor = connection.cursor()
    cursor.execute("SELECT current_database(), version();")

    result = cursor.fetchone()

    print("PostgreSQL Connected Successfully!")
    print("Database:", result[0])
    print("PostgreSQL Version:", result[1])

    cursor.close()
    connection.close()

except Exception as error:
    print("Database connection failed:", error)
