from app.analytics import load_sales_data, get_kpis, group_sales, monthly_sales

def test_sample_data_loads():
    df = load_sales_data()
    assert len(df) > 0
    assert {"order_id", "customer_id", "sales"}.issubset(df.columns)

def test_kpis_are_valid():
    kpis = get_kpis(load_sales_data())
    assert kpis["total_orders"] > 0
    assert kpis["total_revenue"] > 0
    assert kpis["unique_customers"] > 0

def test_grouping_and_monthly_results():
    df = load_sales_data()
    assert len(group_sales(df, "region")) > 0
    assert len(monthly_sales(df)) > 0
