import pandas as pd
import streamlit as st

from query_runner import execute_query


def load_data(sql):
    result = execute_query(sql)
    if not result.get("success"):
        raise RuntimeError(result.get("error", "Unknown database query error."))
    return pd.DataFrame(result.get("rows", []))


def render_operations_dashboard():
    st.subheader("Operations Overview")
    st.caption("Live data from the TrustLens PostgreSQL analytics database.")

    monthly_sql = """
        SELECT order_month, total_orders, delivered_orders, gmv,
               late_delivery_pct, avg_review_score
        FROM analytics.v_monthly_kpis
        ORDER BY order_month;
    """
    state_sql = """
        SELECT c.customer_state,
               COUNT(DISTINCT f.order_id) AS delivered_orders,
               ROUND(100.0 * COUNT(DISTINCT f.order_id)
                   FILTER (WHERE f.is_late = TRUE)
                   / NULLIF(COUNT(DISTINCT f.order_id), 0), 2) AS late_delivery_rate
        FROM analytics.v_order_facts f
        JOIN raw.customers c ON f.customer_id = c.customer_id
        WHERE f.order_status = 'delivered' AND f.is_late IS NOT NULL
        GROUP BY c.customer_state
        ORDER BY late_delivery_rate DESC;
    """

    try:
        monthly = load_data(monthly_sql)
        states = load_data(state_sql)
        if monthly.empty:
            st.info("No monthly KPI data is available.")
            return

        for col in ["total_orders", "delivered_orders", "gmv", "late_delivery_pct", "avg_review_score"]:
            monthly[col] = pd.to_numeric(monthly[col], errors="coerce")

        orders = monthly["total_orders"].sum()
        revenue = monthly["gmv"].sum()
        delivered = monthly["delivered_orders"].sum()
        late_rate = ((monthly["late_delivery_pct"] * monthly["delivered_orders"]).sum() / delivered) if delivered else 0
        review = monthly["avg_review_score"].mean()

        aov = revenue / orders if orders else 0

        a, b, c, d, e = st.columns(5)
        a.metric("Total Sales (GMV)", f"₹{revenue:,.0f}")
        b.metric("Late Delivery Rate", f"{late_rate:.2f}%")
        c.metric("Total Orders", f"{orders:,.0f}")
        d.metric("Average Order Value", f"₹{aov:,.2f}")
        e.metric("Average Review Score", f"{review:.2f}/5" if pd.notna(review) else "N/A")

        left, right = st.columns(2)
        with left:
            st.markdown("#### Monthly Revenue (GMV)")
            st.line_chart(monthly.set_index("order_month")[["gmv"]], use_container_width=True)
        with right:
            st.markdown("#### Monthly Orders")
            st.bar_chart(monthly.set_index("order_month")[["total_orders"]], use_container_width=True)

        left, right = st.columns(2)
        with left:
            st.markdown("#### Monthly Late Delivery Rate")
            st.line_chart(monthly.set_index("order_month")[["late_delivery_pct"]], use_container_width=True)
        with right:
            st.markdown("#### Late Delivery by Customer State")
            if not states.empty:
                states["late_delivery_rate"] = pd.to_numeric(states["late_delivery_rate"], errors="coerce")
                st.bar_chart(states.head(10).set_index("customer_state")[["late_delivery_rate"]], use_container_width=True)
            else:
                st.info("No state-level data is available.")

        with st.expander("View monthly KPI data"):
            st.dataframe(monthly, use_container_width=True, hide_index=True)

    except Exception as error:
        st.error("Operations dashboard data could not be loaded.")
        st.code(str(error))


def render_delivery_analysis():
    from datetime import date

    st.subheader("Delivery Analysis")
    st.caption("Where and why parcels are late, and what this does to reviews.")

    date_col, spacer = st.columns([2, 5])
    with date_col:
        selected_range = st.date_input(
            "Date Range (purchase date)",
            value=(date(2017, 1, 1), date(2018, 8, 31)),
            min_value=date(2016, 9, 1),
            max_value=date(2018, 10, 31),
            key="delivery_date_range"
        )

    if not isinstance(selected_range, (tuple, list)) or len(selected_range) != 2:
        st.info("Choose both a start date and an end date to display delivery analysis.")
        return

    start_date, end_date = selected_range
    if start_date > end_date:
        st.warning("The start date must be before the end date.")
        return

    start_sql = start_date.isoformat()
    end_sql = end_date.isoformat()
    date_filter = f"f.purchase_date::date BETWEEN DATE '{start_sql}' AND DATE '{end_sql}'"

    kpi_sql = f"""
        SELECT
            ROUND(
                100.0 * COUNT(*) FILTER (WHERE f.is_late = TRUE)
                / NULLIF(COUNT(*) FILTER (WHERE f.is_late IS NOT NULL), 0), 2
            ) AS late_delivery_rate,
            ROUND(AVG(
                (NULLIF(TRIM(o.order_delivered_customer_date), '')::date
                 - NULLIF(TRIM(o.order_purchase_timestamp), '')::date)::numeric
            ), 2) AS avg_delivery_days,
            ROUND(AVG(
                (NULLIF(TRIM(o.order_estimated_delivery_date), '')::date
                 - NULLIF(TRIM(o.order_purchase_timestamp), '')::date)::numeric
            ), 2) AS avg_estimated_days
        FROM analytics.v_order_facts f
        JOIN raw.orders o ON f.order_id = o.order_id
        WHERE f.order_status = 'delivered'
          AND {date_filter};
    """

    review_sql = f"""
        SELECT
            ROUND(AVG(r.avg_score) FILTER (WHERE f.is_late = TRUE), 2) AS late_review_score,
            ROUND(AVG(r.avg_score) FILTER (WHERE f.is_late = FALSE), 2) AS ontime_review_score
        FROM analytics.v_order_facts f
        JOIN (
            SELECT order_id, AVG(NULLIF(review_score, '')::numeric) AS avg_score
            FROM raw.order_reviews
            GROUP BY order_id
        ) r ON f.order_id = r.order_id
        WHERE f.order_status = 'delivered'
          AND f.is_late IS NOT NULL
          AND {date_filter};
    """

    monthly_sql = f"""
        SELECT
            TO_CHAR(DATE_TRUNC('month', f.purchase_date), 'YYYY-MM') AS order_month,
            ROUND(AVG(
                (NULLIF(TRIM(o.order_delivered_customer_date), '')::date
                 - NULLIF(TRIM(o.order_purchase_timestamp), '')::date)::numeric
            ), 2) AS actual_delivery_days,
            ROUND(AVG(
                (NULLIF(TRIM(o.order_estimated_delivery_date), '')::date
                 - NULLIF(TRIM(o.order_purchase_timestamp), '')::date)::numeric
            ), 2) AS estimated_delivery_days
        FROM analytics.v_order_facts f
        JOIN raw.orders o ON f.order_id = o.order_id
        WHERE f.order_status = 'delivered'
          AND {date_filter}
        GROUP BY DATE_TRUNC('month', f.purchase_date)
        ORDER BY DATE_TRUNC('month', f.purchase_date);
    """

    bucket_sql = f"""
        SELECT
            CASE
                WHEN (NULLIF(TRIM(o.order_delivered_customer_date), '')::date
                      - NULLIF(TRIM(o.order_estimated_delivery_date), '')::date) <= 2 THEN '0-2 days'
                WHEN (NULLIF(TRIM(o.order_delivered_customer_date), '')::date
                      - NULLIF(TRIM(o.order_estimated_delivery_date), '')::date) <= 5 THEN '3-5 days'
                WHEN (NULLIF(TRIM(o.order_delivered_customer_date), '')::date
                      - NULLIF(TRIM(o.order_estimated_delivery_date), '')::date) <= 10 THEN '6-10 days'
                WHEN (NULLIF(TRIM(o.order_delivered_customer_date), '')::date
                      - NULLIF(TRIM(o.order_estimated_delivery_date), '')::date) <= 15 THEN '11-15 days'
                WHEN (NULLIF(TRIM(o.order_delivered_customer_date), '')::date
                      - NULLIF(TRIM(o.order_estimated_delivery_date), '')::date) <= 20 THEN '16-20 days'
                ELSE '20+ days'
            END AS delay_bucket,
            ROUND(AVG(r.avg_score), 2) AS avg_review_score,
            COUNT(*) AS reviewed_orders
        FROM analytics.v_order_facts f
        JOIN raw.orders o ON f.order_id = o.order_id
        JOIN (
            SELECT order_id, AVG(NULLIF(review_score, '')::numeric) AS avg_score
            FROM raw.order_reviews
            GROUP BY order_id
        ) r ON f.order_id = r.order_id
        WHERE f.order_status = 'delivered'
          AND f.is_late = TRUE
          AND {date_filter}
        GROUP BY 1
        ORDER BY MIN(
            NULLIF(TRIM(o.order_delivered_customer_date), '')::date
            - NULLIF(TRIM(o.order_estimated_delivery_date), '')::date
        );
    """

    category_sql = f"""
        SELECT
            COALESCE(ct.product_category_name_english, p.product_category_name, 'Unknown') AS product_category,
            COUNT(DISTINCT f.order_id) AS delivered_orders,
            COUNT(DISTINCT f.order_id) FILTER (WHERE f.is_late = TRUE) AS late_orders,
            ROUND(
                100.0 * COUNT(DISTINCT f.order_id) FILTER (WHERE f.is_late = TRUE)
                / NULLIF(COUNT(DISTINCT f.order_id) FILTER (WHERE f.is_late IS NOT NULL), 0), 2
            ) AS late_delivery_rate
        FROM analytics.v_order_facts f
        JOIN raw.order_items oi ON f.order_id = oi.order_id
        JOIN raw.products p ON oi.product_id = p.product_id
        LEFT JOIN raw.category_translation ct
            ON p.product_category_name = ct.product_category_name
        WHERE f.order_status = 'delivered'
          AND f.is_late IS NOT NULL
          AND {date_filter}
        GROUP BY 1
        HAVING COUNT(DISTINCT f.order_id) >= 100
        ORDER BY late_delivery_rate DESC
        LIMIT 10;
    """

    state_sql = f"""
        SELECT
            c.customer_state,
            COUNT(DISTINCT f.order_id) AS delivered_orders,
            COUNT(DISTINCT f.order_id) FILTER (WHERE f.is_late = TRUE) AS late_orders,
            ROUND(
                100.0 * COUNT(DISTINCT f.order_id) FILTER (WHERE f.is_late = TRUE)
                / NULLIF(COUNT(DISTINCT f.order_id) FILTER (WHERE f.is_late IS NOT NULL), 0), 2
            ) AS late_delivery_rate
        FROM analytics.v_order_facts f
        JOIN raw.customers c ON f.customer_id = c.customer_id
        WHERE f.order_status = 'delivered'
          AND f.is_late IS NOT NULL
          AND {date_filter}
        GROUP BY c.customer_state
        ORDER BY late_delivery_rate DESC;
    """

    try:
        kpis = load_data(kpi_sql)
        reviews = load_data(review_sql)
        monthly = load_data(monthly_sql)
        buckets = load_data(bucket_sql)
        categories = load_data(category_sql)
        states = load_data(state_sql)

        if kpis.empty:
            st.info("No delivery records found for this date range.")
            return

        kpi = kpis.iloc[0]
        late_score = pd.to_numeric(pd.Series([reviews.iloc[0]["late_review_score"]]), errors="coerce").iloc[0]
        ontime_score = pd.to_numeric(pd.Series([reviews.iloc[0]["ontime_review_score"]]), errors="coerce").iloc[0]
        review_drop = ontime_score - late_score if pd.notna(ontime_score) and pd.notna(late_score) else None

        st.caption(f"Purchase dates: {start_date:%d %b %Y} – {end_date:%d %b %Y}")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Late Delivery Rate", f"{float(kpi['late_delivery_rate'] or 0):.2f}%")
        c2.metric("Avg Delivery Days", f"{float(kpi['avg_delivery_days'] or 0):.2f}")
        c3.metric("Avg Estimated Days", f"{float(kpi['avg_estimated_days'] or 0):.2f}")
        c4.metric("Review Drop When Late", f"{review_drop:.2f}" if review_drop is not None else "N/A")

        st.divider()
        left, right = st.columns(2)
        with left:
            st.markdown("#### Review Score by Delay Bucket")
            if not buckets.empty:
                buckets["avg_review_score"] = pd.to_numeric(buckets["avg_review_score"], errors="coerce")
                st.bar_chart(buckets.set_index("delay_bucket")[["avg_review_score"]], use_container_width=True)
            else:
                st.info("No reviewed late deliveries in this date range.")
        with right:
            st.markdown("#### Top 10 Categories by Late Delivery Rate")
            if not categories.empty:
                categories["late_delivery_rate"] = pd.to_numeric(categories["late_delivery_rate"], errors="coerce")
                st.bar_chart(
                    categories.sort_values("late_delivery_rate").set_index("product_category")[["late_delivery_rate"]],
                    use_container_width=True
                )
            else:
                st.info("No category data found for this date range.")

        st.divider()
        st.markdown("#### Actual vs Estimated Delivery Days by Month")
        if not monthly.empty:
            monthly = monthly.set_index("order_month")
            st.line_chart(monthly[["actual_delivery_days", "estimated_delivery_days"]], use_container_width=True)
        else:
            st.info("No monthly delivery data found.")

        left, right = st.columns([1, 1])
        with left:
            st.markdown("#### State Delivery Table")
            if not states.empty:
                st.dataframe(states, use_container_width=True, hide_index=True)
            else:
                st.info("No state data found.")
        with right:
            st.markdown("#### Delivery Summary")
            st.metric("Late Review Score", f"{late_score:.2f}" if pd.notna(late_score) else "N/A")
            st.metric("On-time Review Score", f"{ontime_score:.2f}" if pd.notna(ontime_score) else "N/A")

    except Exception as error:
        st.error("Delivery analysis data could not be loaded.")
        st.code(str(error))
