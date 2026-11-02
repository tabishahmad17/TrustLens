
from sql_generator import generate_sql
from sql_validator import validate_sql
from query_runner import execute_query
from answer_generator import generate_answer
from audit import log_interaction


def safe_log_interaction(question, sql, status, error=None):
    """Prevent audit logging failures from crashing the assistant."""

    try:
        log_interaction(question, sql, status, error)
    except Exception as logging_error:
        print(f"Audit logging failed: {logging_error}")


def ask_trustlens(question):

    generated_sql = None

    try:

        # 1. Generate SQL
        print("\nGenerating SQL...")
        generated_sql = generate_sql(question)

        print("\nGenerated SQL:")
        print(generated_sql)

        # 2. Validate SQL
        print("\nValidating SQL...")

        is_valid, message = validate_sql(generated_sql)

        if not is_valid:

            safe_log_interaction(
                question,
                generated_sql,
                "failed",
                message
            )

            return {
                "success": False,
                "error": message
            }

        print("SQL validation successful!")

        # 3. Execute SQL in PostgreSQL
        print("\nExecuting query...")

        result = execute_query(generated_sql)

        if not result["success"]:

            safe_log_interaction(
                question,
                generated_sql,
                "failed",
                result["error"]
            )

            return result

        # 4. Generate business explanation
        print("\nGenerating business explanation...")

        answer = generate_answer(
            question,
            generated_sql,
            result["rows"]
        )

        # 5. Record successful interaction
        safe_log_interaction(
            question,
            generated_sql,
            "success"
        )

        return {
            "success": True,
            "answer": answer,
            "sql": generated_sql,
            "columns": result["columns"],
            "rows": result["rows"],
            "row_count": result["row_count"]
        }

    except Exception as error:

        safe_log_interaction(
            question,
            generated_sql,
            "failed",
            str(error)
        )

        return {
            "success": False,
            "error": str(error)
        }


if __name__ == "__main__":

    question = input(
        "\nAsk TrustLens a business question: "
    )

    result = ask_trustlens(question)

    if result["success"]:

        print("\n========== TRUSTLENS ANSWER ==========")
        print(result["answer"])

        print("\n========== SQL QUERY ==========")
        print(result["sql"])

        print("\n========== ROW COUNT ==========")
        print(result["row_count"])

    else:
        print("\nError:", result["error"])
