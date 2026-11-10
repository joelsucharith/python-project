# Filtering and Data Analysis

This guide describes how transaction filtering and spending reports work in Bunny Budget.

## Transaction filtering

The transaction screen loads the expense list and filters it in the browser. All selected filters are combined, so an expense must match every active filter:

- **Search** checks the description and notes without regard to letter case. Empty descriptions and notes do not cause errors.
- **Category** matches one exact category. The empty selection includes every category.
- **From date** includes expenses on or after the selected date.
- **To date** includes expenses on or before the selected date.
- Results are ordered newest first; transactions on the same date are ordered by descending expense ID.

The browser compares ISO date strings (`YYYY-MM-DD`), which sort chronologically as text. The date inputs provide this format.

### Expense API filters

`GET /api/expenses` supports optional query parameters. They can be combined, and the server applies them using AND logic:

| Parameter | Behavior |
|---|---|
| `month=YYYY-MM` | Includes dates from the first through the last day of that month. |
| `category=name` | Matches the category name exactly. |
| `search=text` | Searches descriptions and notes. `%`, `_` and backslash are treated as literal characters, not caller-supplied SQL wildcards. |
| `from=YYYY-MM-DD` | Includes the given date and later dates. |
| `to=YYYY-MM-DD` | Includes the given date and earlier dates. |

Example: `GET /api/expenses?month=2026-10&category=Food&from=2026-10-01&to=2026-10-31` returns October Food expenses. Invalid months and dates return HTTP 400 with a JSON `error` field. SQL values are passed as query parameters rather than interpolated into SQL.

The screen's search/category/date controls filter the already-loaded list locally. They do not request the API again. The selected report month controls the dashboard and analytics, but does not restrict the transaction list.

## Reports and calculations

The dashboard computes the following values from its loaded expense data:

- **Monthly total:** sum of expense amounts dated in the selected month.
- **All-time total:** sum of all loaded expenses, regardless of selected month.
- **Transaction count:** number of expenses in the selected month.
- **Daily average:** monthly total divided by the current day number for the current month; for another selected month, divided by that month's number of calendar days.
- **Category report and pie chart:** sum amounts by category for the selected month. Each category's share is its total divided by the month's total.
- **Monthly trend:** totals for the selected month and five preceding calendar months.
- **Budget remaining:** selected month's budget minus its spending. The progress indicator is capped visually at 100%; spending above budget is still shown as a negative remaining amount.

The `GET /api/summary?month=YYYY-MM` endpoint returns the selected month's total, transaction count, all-time total, budget and category totals. If `month` is omitted, the current month is used. The CSV export includes all expenses in date order; it is not affected by the transaction screen filters or selected report month.

Amounts are stored as MySQL `DECIMAL(10,2)`. The browser sums integer paise (hundredths of a rupee) to avoid common floating-point addition errors.

## Tests

Run the API behavior tests with:

```bash
python -m unittest -v test_app
```

They use Flask's test client and mock database functions, so they check filter construction, input validation and summary response formatting without requiring a running MySQL server. They do not replace an integration test against a configured database.
