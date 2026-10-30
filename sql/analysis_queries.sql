-- Example SQL queries for a sales table with the same columns as sample_sales.csv.

-- 1. Revenue, order count and average order value
SELECT
    SUM(sales) AS total_revenue,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(sales) / NULLIF(COUNT(DISTINCT order_id), 0) AS average_order_value
FROM sales;

-- 2. Revenue by region
SELECT region, SUM(sales) AS revenue
FROM sales
GROUP BY region
ORDER BY revenue DESC;

-- 3. Monthly revenue
SELECT
    strftime('%Y-%m', order_date) AS sales_month,
    SUM(sales) AS revenue
FROM sales
GROUP BY strftime('%Y-%m', order_date)
ORDER BY sales_month;

-- 4. Customer ranking with a window function
WITH customer_totals AS (
    SELECT customer_id, SUM(sales) AS total_spend
    FROM sales
    GROUP BY customer_id
)
SELECT
    customer_id,
    total_spend,
    DENSE_RANK() OVER (ORDER BY total_spend DESC) AS customer_rank
FROM customer_totals
ORDER BY customer_rank;
