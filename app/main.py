from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from app.analytics import load_sales_data, get_kpis, group_sales, monthly_sales

app = FastAPI(
    title="AI-Powered Sales & Customer Analytics Platform",
    description="A learning project for sales analytics with Python, Pandas, SQL and FastAPI.",
    version="1.0.0"
)

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!doctype html><html><head><title>Sales Analytics</title>
    <style>
    body{font-family:Arial,sans-serif;max-width:900px;margin:40px auto;padding:0 18px;color:#1f2937}
    h1{color:#17365d}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px}
    .card{border:1px solid #d9e0e8;border-radius:9px;padding:16px}.value{font-size:24px;font-weight:bold}
    a{color:#175cd3}button{padding:9px 14px;background:#175cd3;color:white;border:0;border-radius:5px}
    </style></head><body>
    <h1>Sales & Customer Analytics</h1>
    <p>Demo dashboard using a synthetic sample dataset (300 orders).</p>
    <button onclick="loadKpis()">Refresh KPIs</button>
    <div id="kpis" class="grid"></div>
    <h2>Revenue by region</h2><pre id="regions">Click Refresh KPIs.</pre>
    <p><a href="/docs">Open API documentation</a></p>
    <script>
    async function loadKpis(){
      const r=await fetch('/analytics/kpis'); const d=await r.json();
      document.getElementById('kpis').innerHTML=Object.entries(d).map(([k,v])=>
        `<div class="card"><div>${k.replaceAll('_',' ')}</div><div class="value">${typeof v==='number'?v.toLocaleString():v}</div></div>`).join('');
      const rr=await fetch('/analytics/by-region');
      document.getElementById('regions').textContent=JSON.stringify(await rr.json(),null,2);
    }
    loadKpis();
    </script></body></html>
    """

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/analytics/kpis")
def analytics_kpis():
    try:
        return get_kpis(load_sales_data())
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@app.get("/analytics/by-region")
def by_region():
    return group_sales(load_sales_data(), "region")

@app.get("/analytics/by-product")
def by_product():
    return group_sales(load_sales_data(), "product")

@app.get("/analytics/by-channel")
def by_channel():
    return group_sales(load_sales_data(), "channel")

@app.get("/analytics/monthly")
def by_month():
    return monthly_sales(load_sales_data())

@app.get("/analytics/search-customer")
def search_customer(customer_id: str = Query(..., min_length=1)):
    df = load_sales_data()
    result = df[df["customer_id"].str.lower() == customer_id.lower()]
    if result.empty:
        raise HTTPException(status_code=404, detail="Customer not found in the sample dataset.")
    return {
        "customer_id": customer_id,
        "orders": int(result["order_id"].nunique()),
        "total_spend": round(float(result["sales"].sum()), 2),
        "orders_detail": [
            {"order_id": r.order_id, "date": r.order_date.strftime("%Y-%m-%d"),
             "product": r.product, "sales": round(float(r.sales), 2)}
            for r in result.itertuples()
        ]
    }
