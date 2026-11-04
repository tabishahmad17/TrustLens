
-- TrustLens: Customer Satisfaction Analysis

-- 1. Overall review score
SELECT
    COUNT(*) AS review_rows,
    ROUND(AVG(NULLIF(TRIM(review_score), '')::numeric), 2)
        AS avg_review_score
FROM raw.order_reviews;


-- 2. Average rating by delivery group
SELECT
    CASE
        WHEN o.is_late = TRUE THEN 'Late'
        WHEN o.is_late = FALSE THEN 'Early or on-time'
    END AS delivery_group,
    COUNT(*) AS reviewed_orders,
    ROUND(AVG(r.review_score), 2)
        AS avg_review_score
FROM analytics.v_order_facts AS o
JOIN (
    SELECT
        order_id,
        AVG(NULLIF(TRIM(review_score), '')::numeric) AS review_score
    FROM raw.order_reviews
    WHERE NULLIF(review_score, '') IS NOT NULL
    GROUP BY order_id
) AS r
    ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
  AND o.is_late IS NOT NULL
GROUP BY 1
ORDER BY avg_review_score;


-- 3. Executive summary
SELECT
    COUNT(*) AS reviewed_delivered_orders,
    COUNT(*) FILTER (
        WHERE o.is_late = TRUE
    ) AS late_orders,
    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE o.is_late = TRUE
        ) / NULLIF(COUNT(*) FILTER (WHERE o.is_late IS NOT NULL), 0),
        2
    ) AS late_delivery_pct,
    ROUND(
        AVG(r.review_score) FILTER (
            WHERE o.is_late = TRUE
        ),
        2
    ) AS late_order_rating,
    ROUND(
        AVG(r.review_score) FILTER (
            WHERE o.is_late = FALSE
        ),
        2
    ) AS early_order_rating
FROM analytics.v_order_facts AS o
JOIN (
    SELECT
        order_id,
        AVG(NULLIF(TRIM(review_score), '')::numeric) AS review_score
    FROM raw.order_reviews
    WHERE NULLIF(review_score, '') IS NOT NULL
    GROUP BY order_id
) AS r
    ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
  AND o.is_late IS NOT NULL;
