-- Query 1: Monthly Business Performance

SELECT
    order_month,
    total_orders,
    delivered_orders,
    ROUND(gmv::NUMERIC, 2) AS total_revenue,
    ROUND(aov::NUMERIC, 2) AS average_order_value,
    ROUND(late_delivery_pct::NUMERIC, 2) AS late_delivery_rate,
    ROUND(avg_review_score::NUMERIC, 2) AS average_review_score
FROM analytics.v_monthly_kpis
ORDER BY order_month;

-- Query 2: Top Product Categories by Revenue

SELECT
    COALESCE(
        ct.product_category_name_english,
        p.product_category_name,
        'Unknown'
    ) AS category_name,

    COUNT(DISTINCT oi.order_id) AS total_orders,

    ROUND(
        SUM(NULLIF(TRIM(oi.price), '')::NUMERIC),
        2
    ) AS total_revenue

FROM raw.order_items oi

JOIN raw.orders o
    ON oi.order_id = o.order_id

JOIN raw.products p
    ON oi.product_id = p.product_id

LEFT JOIN raw.category_translation ct
    ON p.product_category_name = ct.product_category_name

WHERE o.order_status = 'delivered'

GROUP BY 1

ORDER BY total_revenue DESC

LIMIT 10;


-- Query 3: Top 10 Sellers by Revenue

SELECT
    oi.seller_id,
    s.seller_city,
    s.seller_state,

    COUNT(DISTINCT oi.order_id) AS total_orders,

    ROUND(
        SUM(NULLIF(TRIM(oi.price), '')::NUMERIC),
        2
    ) AS total_revenue

FROM raw.order_items oi

JOIN raw.orders o
    ON oi.order_id = o.order_id

JOIN raw.sellers s
    ON oi.seller_id = s.seller_id

WHERE o.order_status = 'delivered'

GROUP BY
    oi.seller_id,
    s.seller_city,
    s.seller_state

ORDER BY total_revenue DESC

LIMIT 10;


-- Query 4: State-wise Late Delivery Analysis

SELECT
    c.customer_state,

    COUNT(DISTINCT f.order_id) AS total_delivered_orders,

    COUNT(DISTINCT f.order_id)
        FILTER (WHERE f.is_late = TRUE) AS late_orders,

    ROUND(
        100.0 * COUNT(DISTINCT f.order_id)
            FILTER (WHERE f.is_late = TRUE)
        / NULLIF(COUNT(DISTINCT f.order_id)
            FILTER (WHERE f.is_late IS NOT NULL), 0),
        2
    ) AS late_delivery_rate

FROM analytics.v_order_facts f

JOIN raw.customers c
    ON f.customer_id = c.customer_id

WHERE f.order_status = 'delivered'
  AND f.is_late IS NOT NULL

GROUP BY c.customer_state

ORDER BY late_delivery_rate DESC;


-- Query 5: Customer Satisfaction - Late vs On-time Delivery

WITH review_per_order AS (
    SELECT
        order_id,
        AVG(review_score::NUMERIC) AS average_review_score
    FROM raw.order_reviews
    GROUP BY order_id
)

SELECT
    CASE
        WHEN f.is_late = TRUE THEN 'Late Delivery'
        WHEN f.is_late = FALSE THEN 'On-time Delivery'
    END AS delivery_status,

    COUNT(DISTINCT f.order_id) AS total_orders,

    ROUND(
        AVG(r.average_review_score)::NUMERIC,
        2
    ) AS average_review_score

FROM analytics.v_order_facts f

JOIN review_per_order r
    ON f.order_id = r.order_id

WHERE f.order_status = 'delivered'
  AND f.is_late IS NOT NULL

GROUP BY f.is_late

ORDER BY f.is_late DESC;

-- QUERY 6: Payment Method Analysis
-- Business question: Which payment methods are most commonly used?

SELECT
    payment_type,
    COUNT(*) AS total_transactions,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(
        SUM(payment_value::NUMERIC), 2
    ) AS total_payment_value
FROM raw.order_payments
GROUP BY payment_type
ORDER BY total_payment_value DESC;


-- QUERY 7: Monthly Order Cancellation Analysis
-- Business question: How does the cancellation rate change over time?

SELECT
    DATE_TRUNC(
        'month',
        NULLIF(order_purchase_timestamp, '')::TIMESTAMP
    )::DATE AS order_month,
    COUNT(*) AS total_orders,
    COUNT(*) FILTER (
        WHERE order_status = 'canceled'
    ) AS cancelled_orders,
    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE order_status = 'canceled'
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS cancellation_rate
FROM raw.orders
WHERE NULLIF(order_purchase_timestamp, '') IS NOT NULL
GROUP BY 1
ORDER BY 1;


-- QUERY 8: State-wise Revenue Analysis
-- Business question: Which customer states generate the most revenue?

SELECT
    c.customer_state,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(
        SUM(NULLIF(TRIM(oi.price), '')::NUMERIC), 2
    ) AS total_revenue
FROM raw.orders o
JOIN raw.customers c
    ON o.customer_id = c.customer_id
JOIN raw.order_items oi
    ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
GROUP BY c.customer_state
ORDER BY total_revenue DESC;


-- QUERY 9: Product Category Late Delivery Analysis
-- Business question: Which categories are associated with more late orders?

SELECT
    COALESCE(
        ct.product_category_name_english,
        p.product_category_name,
        'Unknown'
    ) AS category_name,
    COUNT(DISTINCT f.order_id) AS total_delivered_orders,
    COUNT(DISTINCT f.order_id)
        FILTER (WHERE f.is_late = TRUE) AS late_orders,
    ROUND(
        100.0 * COUNT(DISTINCT f.order_id)
            FILTER (WHERE f.is_late = TRUE)
        / NULLIF(COUNT(DISTINCT f.order_id), 0),
        2
    ) AS late_delivery_rate
FROM analytics.v_order_facts f
JOIN raw.order_items oi
    ON f.order_id = oi.order_id
JOIN raw.products p
    ON oi.product_id = p.product_id
LEFT JOIN raw.category_translation ct
    ON p.product_category_name = ct.product_category_name
WHERE f.order_status = 'delivered'
  AND f.is_late IS NOT NULL
GROUP BY 1
ORDER BY late_delivery_rate DESC;


-- QUERY 10: Top 10 Sellers by Late Deliveries
-- Business question: Which sellers contribute the most late orders?

SELECT
    oi.seller_id,
    s.seller_city,
    s.seller_state,
    COUNT(DISTINCT f.order_id) AS total_delivered_orders,
    COUNT(DISTINCT f.order_id)
        FILTER (WHERE f.is_late = TRUE) AS late_orders,
    ROUND(
        100.0 * COUNT(DISTINCT f.order_id)
            FILTER (WHERE f.is_late = TRUE)
        / NULLIF(COUNT(DISTINCT f.order_id), 0),
        2
    ) AS late_delivery_rate
FROM analytics.v_order_facts f
JOIN raw.order_items oi
    ON f.order_id = oi.order_id
JOIN raw.sellers s
    ON oi.seller_id = s.seller_id
WHERE f.order_status = 'delivered'
  AND f.is_late IS NOT NULL
GROUP BY
    oi.seller_id,
    s.seller_city,
    s.seller_state
ORDER BY late_orders DESC
LIMIT 10;