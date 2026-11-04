import unittest

from sql_validator import validate_sql


class SQLValidatorTests(unittest.TestCase):
    def assert_allowed(self, query):
        valid, message = validate_sql(query)
        self.assertTrue(valid, message)

    def assert_rejected(self, query):
        valid, _ = validate_sql(query)
        self.assertFalse(valid)

    def test_allows_approved_schema_table(self):
        self.assert_allowed("SELECT * FROM raw.orders")

    def test_allows_approved_analytics_view(self):
        self.assert_allowed("SELECT * FROM analytics.v_monthly_kpis")

    def test_allows_aggregate_query(self):
        self.assert_allowed(
            "SELECT customer_state, COUNT(*) "
            "FROM raw.customers GROUP BY customer_state"
        )

    def test_allows_cte_using_approved_table(self):
        self.assert_allowed(
            "WITH recent_orders AS ("
            "SELECT order_id FROM raw.orders"
            ") SELECT * FROM recent_orders"
        )

    def test_rejects_delete(self):
        self.assert_rejected("DELETE FROM raw.orders")

    def test_rejects_unapproved_table(self):
        self.assert_rejected("SELECT * FROM raw.secret_table")

    def test_rejects_unqualified_table(self):
        self.assert_rejected("SELECT * FROM orders")

    def test_rejects_multiple_statements(self):
        self.assert_rejected("SELECT * FROM raw.orders; SELECT * FROM raw.customers")

    def test_rejects_dangerous_function(self):
        self.assert_rejected("SELECT pg_sleep(5)")

    def test_rejects_schema_qualified_function(self):
        self.assert_rejected("SELECT public.some_function()")

    def test_rejects_cross_database_reference(self):
        self.assert_rejected("SELECT * FROM otherdb.raw.orders")


if __name__ == "__main__":
    unittest.main()
