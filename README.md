# AI-Powered Sales & Customer Analytics Platform

A beginner-friendly analytics project built with **Python, Pandas, SQL concepts and FastAPI**. It loads a sample sales dataset, validates the records, calculates business KPIs and exposes analytics through REST API endpoints.

> **Dataset note:** `data/sample_sales.csv` is synthetic demonstration data generated for this repository. It is not a real company dataset and does not substantiate any claim about 10,000+ real sales records. Replace it with the original project dataset only if you have permission to share it.

## Features

- Load and validate sales records with Pandas.
- Calculate total revenue, orders, customers, units sold and average order value.
- Analyse revenue by region, product and sales channel.
- Calculate monthly revenue.
- Search sample customer purchase summaries.
- Expose analytics through FastAPI.
- Include SQL examples using CTEs and window functions.

## Technology stack

- Python 3.10+
- Pandas
- FastAPI
- SQL (example queries)
- Uvicorn
- Pytest

## Project structure

```text
ai-sales-customer-analytics/
├── app/
│   ├── __init__.py
│   ├── analytics.py
│   └── main.py
├── data/
│   └── sample_sales.csv
├── sql/
│   └── analysis_queries.sql
├── tests/
│   └── test_analytics.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Run locally

### 1. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\\Scripts\\activate
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the API

```bash
uvicorn app.main:app --reload
```

Open the dashboard at http://127.0.0.1:8000 and API documentation at http://127.0.0.1:8000/docs.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | API health check |
| GET | `/analytics/kpis` | Overall sales KPIs |
| GET | `/analytics/by-region` | Revenue by region |
| GET | `/analytics/by-product` | Revenue by product |
| GET | `/analytics/by-channel` | Revenue by channel |
| GET | `/analytics/monthly` | Monthly revenue |
| GET | `/analytics/search-customer?customer_id=CUST-001` | Sample customer summary |

## Run tests

```bash
pytest -q
```

## SQL analysis

See `sql/analysis_queries.sql` for examples of aggregation, CTEs and window functions. The API currently calculates results from the CSV using Pandas; it does not yet connect to a production SQL database.

## Power BI and Tableau

The CSV can be imported into Power BI or Tableau to build visualisations. Suggested visuals:
- KPI cards for revenue, orders and customers
- Monthly revenue line chart
- Revenue by region bar chart
- Product and channel breakdowns

No Power BI or Tableau dashboard file is included in this repository yet.

## Limitations and next steps

- The included dataset is synthetic and contains 300 generated orders.
- This version is a working analytics foundation, not an AI/ML prediction system.
- SQL queries are examples and are not wired to a database connection.
- Add dashboard files only after creating and validating them.
- For a real portfolio, document the original dataset, methodology and measured findings.

## Author

Manasa Naram
