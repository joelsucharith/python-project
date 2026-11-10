# Bunny Budget - Personal Expense Tracking and Analysis System

Flask + MySQL expense tracker with a slide-based dashboard (Chart.js charts).

Profile: [lokeshdevarakonda111-commits](https://github.com/lokeshdevarakonda111-commits)

Project repositories: [Original repository](https://github.com/joelsucharith/python-project) · [Personal copy](https://github.com/lokeshdevarakonda111-commits/python-project)

## Folder structure
```
python-project/
├── app.py             Flask routes / REST API
├── auth.py            Login, signup, guest access and session checks
├── db.py              MySQL connection helpers and database setup
├── config.py          Reads database settings from .env
├── schema.sql         Tables and fictional sample data
├── test_app.py        API filter and analysis tests
├── requirements.txt
├── .env.example       Example database configuration
├── templates/         HTML pages
└── static/            CSS and JavaScript for the interface
```

## Setup
```bash
python -m venv venv
source venv/bin/activate           # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
1. Copy `.env.example` to `.env` and set the MySQL connection values, including `DB_PASSWORD`.
2. Create the database, tables and sample data: `python db.py`. **This resets the expense, budget and category tables.**
3. Run the tests: `python -m unittest -v test_app`.
4. Start the website with `python app.py`, then open http://127.0.0.1:5000.

Requires MySQL 8.0.16+ for enforced CHECK constraints. The API tests mock database access and can run without a MySQL server; running the application requires a configured MySQL database.

## Database schema
| Table | Columns |
|---|---|
| categories | category_id (PK), category_name (unique) |
| expenses | expense_id (PK), expense_date, category_id (FK), amount (> 0), description, notes |
| budgets | budget_month (PK, 'YYYY-MM'), amount (>= 0) |

`categories (1) ──< expenses (many)`. A category that still has expenses cannot be deleted.

## API endpoints
| Method | URL | Purpose |
|---|---|---|
| GET | /api/health | database connection check |
| GET | /api/categories | list categories |
| GET | /api/expenses | list; filters `month`, `category`, `search`, `from`, `to` |
| POST | /api/expenses | add (amount must be > 0) |
| PUT | /api/expenses/<id> | edit |
| DELETE | /api/expenses/<id> | delete |
| GET | /api/budgets | all monthly budgets |
| PUT | /api/budgets/<YYYY-MM> | set budget (0 removes it) |
| GET | /api/summary?month=YYYY-MM | month total, count, all-time total, per-category totals |
| GET | /api/export.csv | download all expenses as CSV |

See [FILTERING_AND_ANALYSIS.md](FILTERING_AND_ANALYSIS.md) for filter behavior, report calculations and API examples.

## Limitations
Single-user learning project with fictional sample data. Not a banking or financial-advice system.
