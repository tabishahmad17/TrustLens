
-- TrustLens: Delivery Performance Analysis

-- 1. Overall delivery performance
SELECT
    COUNT(*) AS delivered_orders,
    COUNT(*) FILTER (
        WHERE is_late = TRUE
    ) AS late_orders,
    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE is_late = TRUE
        ) / COUNT(*),
        2
    ) AS late_delivery_pct
FROM analytics.v_order_facts
WHERE order_status = 'delivered';


-- 2. Monthly late-delivery rates
SELECT
    TO_CHAR(purchase_date, 'YYYY-MM') AS order_month,
    COUNT(*) AS delivered_orders,
    COUNT(*) FILTER (
        WHERE is_late = TRUE
    ) AS late_orders,
    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE is_late = TRUE
        ) / COUNT(*),
        2
    ) AS late_delivery_pct
FROM analytics.v_order_facts
WHERE order_status = 'delivered'
  AND purchase_date IS NOT NULL
GROUP BY DATE_TRUNC('month', purchase_date)
HAVING COUNT(*) >= 500
ORDER BY late_delivery_pct DESC;


-- 3. Late deliveries by customer state
SELECT
    c.customer_state,
    COUNT(*) AS delivered_orders,
    COUNT(*) FILTER (
        WHERE o.is_late = TRUE
    ) AS late_orders,
    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE o.is_late = TRUE
        ) / COUNT(*),
        2
    ) AS late_delivery_pct
FROM analytics.v_order_facts AS o
JOIN raw.customers AS c
    ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered'
GROUP BY c.customer_state
HAVING COUNT(*) >= 500
ORDER BY late_delivery_pct DESC;


-- 4. Late deliveries by product category
SELECT
    COALESCE(
        ct.product_category_name_english,
        p.product_category_name,
        'unknown'
    ) AS product_category,
    COUNT(DISTINCT o.order_id) AS delivered_orders,
    COUNT(DISTINCT o.order_id)
        FILTER (WHERE o.is_late = TRUE) AS late_orders,
    ROUND(
        100.0 * COUNT(DISTINCT o.order_id)
            FILTER (WHERE o.is_late = TRUE)
        / NULLIF(COUNT(DISTINCT o.order_id), 0),
        2
    ) AS late_delivery_pct
FROM analytics.v_order_facts AS o
JOIN raw.order_items AS oi
    ON o.order_id = oi.order_id
JOIN raw.products AS p
    ON oi.product_id = p.product_id
LEFT JOIN raw.category_translation AS ct
    ON p.product_category_name = ct.product_category_name
WHERE o.order_status = 'delivered'
GROUP BY 1
HAVING COUNT(DISTINCT o.order_id) >= 100
ORDER BY late_orders DESC
LIMIT 10;


-- 5. Seller delivery performance
SELECT *
FROM analytics.v_seller_performance
WHERE delivered_orders >= 20
ORDER BY late_orders DESC
LIMIT 10;
