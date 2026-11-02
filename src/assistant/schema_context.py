
from db_connection import get_db_connection


def get_schema_context():

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            table_schema,
            table_name,
            column_name,
            data_type
        FROM information_schema.columns
        WHERE table_schema IN ('raw', 'analytics')
        ORDER BY table_schema, table_name, ordinal_position;
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    schema = {}

    for table_schema, table_name, column_name, data_type in rows:

        table = f"{table_schema}.{table_name}"

        if table not in schema:
            schema[table] = []

        schema[table].append(
            f"{column_name} ({data_type})"
        )

    cursor.close()
    connection.close()

    schema_text = ""

    for table, columns in schema.items():
        schema_text += f"\nTable: {table}\n"
        schema_text += "Columns: " + ", ".join(columns) + "\n"

    return schema_text


if __name__ == "__main__":
    print(get_schema_context())
