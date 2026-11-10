import unittest
from unittest.mock import patch

with patch("db.execute"):
    import app as app_module


class ExpenseFilterTests(unittest.TestCase):
    def setUp(self):
        app_module.app.config.update(TESTING=True)
        self.client = app_module.app.test_client()
        with self.client.session_transaction() as session:
            session["user"] = {"id": 1, "name": "Test", "guest": True}

    @patch("app.fetch_all")
    def test_expense_filters_are_combined_and_parameterized(self, fetch_all):
        response = self.client.get(
            "/api/expenses?month=2026-10&category=Food&search=100%25_%5Cmilk"
            "&from=2026-10-01&to=2026-10-31"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])
        query, params = fetch_all.call_args.args
        self.assertIn("e.expense_date BETWEEN %s AND %s", query)
        self.assertIn("c.category_name = %s", query)
        self.assertIn("e.description LIKE %s OR e.notes LIKE %s", query)
        self.assertEqual(
            params,
            (
                "2026-10-01",
                "2026-10-31",
                "Food",
                "%100\\%\\_\\\\milk%",
                "%100\\%\\_\\\\milk%",
                "2026-10-01",
                "2026-10-31",
            ),
        )

    @patch("app.fetch_all")
    def test_invalid_month_is_rejected_before_query(self, fetch_all):
        response = self.client.get("/api/expenses?month=2026-13")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Month must be in YYYY-MM format."})
        fetch_all.assert_not_called()

    @patch("app.fetch_all")
    def test_invalid_date_filter_is_rejected_before_query(self, fetch_all):
        response = self.client.get("/api/expenses?from=2026-02-30")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {"error": "'from' must be a valid date (YYYY-MM-DD)."},
        )
        fetch_all.assert_not_called()


class SummaryTests(unittest.TestCase):
    def setUp(self):
        app_module.app.config.update(TESTING=True)
        self.client = app_module.app.test_client()
        with self.client.session_transaction() as session:
            session["user"] = {"id": 1, "name": "Test", "guest": True}

    @patch("app.fetch_all")
    @patch("app.fetch_one")
    def test_summary_returns_month_totals_budget_and_category_breakdown(
        self, fetch_one, fetch_all
    ):
        fetch_one.side_effect = [
            {"total": 125.5, "cnt": 2},
            {"total": 900.75},
            {"amount": 200},
        ]
        fetch_all.return_value = [
            {"category_name": "Food", "total": 100.25},
            {"category_name": "Travel", "total": 25.25},
        ]

        response = self.client.get("/api/summary?month=2026-10")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json(),
            {
                "month": "2026-10",
                "month_total": 125.5,
                "transaction_count": 2,
                "all_time_total": 900.75,
                "budget": 200.0,
                "by_category": [
                    {"category": "Food", "total": 100.25},
                    {"category": "Travel", "total": 25.25},
                ],
            },
        )
        self.assertEqual(fetch_one.call_args_list[0].args[1], ("2026-10-01", "2026-10-31"))
        self.assertEqual(fetch_all.call_args.args[1], ("2026-10-01", "2026-10-31"))


if __name__ == "__main__":
    unittest.main()