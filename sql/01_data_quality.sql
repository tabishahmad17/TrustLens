-- TrustLens: Data Quality Checks

-- 1. Check row counts
SELECT 'orders' AS table_name, COUNT(*) AS total_rows
FROM raw.orders
UNION ALL
SELECT 'customers', COUNT(*) FROM raw.customers
UNION ALL
SELECT 'order_items', COUNT(*) FROM raw.order_items
UNION ALL
SELECT 'order_payments', COUNT(*) FROM raw.order_payments
UNION ALL
SELECT 'order_reviews', COUNT(*) FROM raw.order_reviews
UNION ALL
SELECT 'products', COUNT(*) FROM raw.products
UNION ALL
SELECT 'sellers', COUNT(*) FROM raw.sellers
UNION ALL
SELECT 'geolocation', COUNT(*) FROM raw.geolocation
UNION ALL
SELECT 'category_translation', COUNT(*) FROM raw.category_translation;


-- 2. Check order ID uniqueness
SELECT
    COUNT(*) AS total_orders,
    COUNT(DISTINCT order_id) AS unique_orders,
    COUNT(*) - COUNT(order_id) AS missing_order_ids
FROM raw.orders;


-- 3. Check missing delivery dates
SELECT
    COUNT(*) FILTER (
        WHERE order_delivered_customer_date = ''
    ) AS missing_delivery_dates,
    COUNT(*) FILTER (
        WHERE order_estimated_delivery_date = ''
    ) AS missing_estimated_dates
FROM raw.orders;

-- TrustLens Data Quality Validation
-- Dataset: Olist Brazilian E-commerce
-- Status: Initial checks completed
-- Known issue: 8 delivered orders have missing actual delivery dates.