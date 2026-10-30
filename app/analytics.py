from pathlib import Path
import pandas as pd

DEFAULT_DATA = Path(__file__).resolve().parent.parent / "data" / "sample_sales.csv"

REQUIRED_COLUMNS = {
    "order_id", "order_date", "customer_id", "region",
    "product", "channel", "quantity", "unit_price", "sales"
}

def load_sales_data(path: str | Path = DEFAULT_DATA) -> pd.DataFrame:
    """Load and validate the sales CSV."""
    df = pd.read_csv(path)
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    for column in ["quantity", "unit_price", "sales"]:
        df[column] = pd.to_numeric(df[column], errors="coerce")
    df = df.dropna(subset=["order_date", "quantity", "unit_price", "sales"])
    df = df[df["quantity"] > 0]
    return df

def get_kpis(df: pd.DataFrame) -> dict:
    """Calculate core sales KPIs from the validated dataset."""
    revenue = float(df["sales"].sum())
    orders = int(df["order_id"].nunique())
    customers = int(df["customer_id"].nunique())
    units = int(df["quantity"].sum())
    return {
        "total_revenue": round(revenue, 2),
        "total_orders": orders,
        "unique_customers": customers,
        "units_sold": units,
        "average_order_value": round(revenue / orders, 2) if orders else 0.0,
        "average_units_per_order": round(units / orders, 2) if orders else 0.0,
        "regions": int(df["region"].nunique()),
        "products": int(df["product"].nunique())
    }

def group_sales(df: pd.DataFrame, column: str) -> list[dict]:
    if column not in {"region", "product", "channel"}:
        raise ValueError("Grouping is allowed only by region, product or channel.")
    result = (
        df.groupby(column, as_index=False)
          .agg(revenue=("sales", "sum"), orders=("order_id", "nunique"), units=("quantity", "sum"))
          .sort_values("revenue", ascending=False)
    )
    return [
        {
            column: str(row[column]),
            "revenue": round(float(row["revenue"]), 2),
            "orders": int(row["orders"]),
            "units": int(row["units"])
        }
        for _, row in result.iterrows()
    ]

def monthly_sales(df: pd.DataFrame) -> list[dict]:
    work = df.copy()
    work["month"] = work["order_date"].dt.to_period("M").astype(str)
    result = work.groupby("month", as_index=False)["sales"].sum().sort_values("month")
    return [{"month": row["month"], "revenue": round(float(row["sales"]), 2)}
            for _, row in result.iterrows()]
