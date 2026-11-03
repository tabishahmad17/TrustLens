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
    st.subheader("Delivery Analysis")
    st.caption("Investigate delivery delays by month, customer state and product category.")

    monthly_sql = """
        SELECT order_month, delivered_orders, late_delivery_pct
        FROM analytics.v_monthly_kpis
        ORDER BY order_month;
    """
    state_sql = """
        SELECT c.customer_state,
               COUNT(DISTINCT f.order_id) AS delivered_orders,
               COUNT(DISTINCT f.order_id) FILTER (WHERE f.is_late = TRUE) AS late_orders,
               ROUND(
                   100.0 * COUNT(DISTINCT f.order_id) FILTER (WHERE f.is_late = TRUE)
                   / NULLIF(COUNT(DISTINCT f.order_id), 0), 2
               ) AS late_delivery_rate
        FROM analytics.v_order_facts f
        JOIN raw.customers c ON f.customer_id = c.customer_id
        WHERE f.order_status = 'delivered' AND f.is_late IS NOT NULL
        GROUP BY c.customer_state
        ORDER BY late_delivery_rate DESC;
    """
    category_sql = """
        SELECT
            COALESCE(ct.product_category_name_english, p.product_category_name, 'Unknown') AS product_category,
            COUNT(DISTINCT f.order_id) AS delivered_orders,
            COUNT(DISTINCT f.order_id) FILTER (WHERE f.is_late = TRUE) AS late_orders,
            ROUND(
                100.0 * COUNT(DISTINCT f.order_id) FILTER (WHERE f.is_late = TRUE)
                / NULLIF(COUNT(DISTINCT f.order_id), 0), 2
            ) AS late_delivery_rate
        FROM analytics.v_order_facts f
        JOIN raw.order_items oi ON f.order_id = oi.order_id
        JOIN raw.products p ON oi.product_id = p.product_id
        LEFT JOIN raw.category_translation ct
            ON p.product_category_name = ct.product_category_name
        WHERE f.order_status = 'delivered' AND f.is_late IS NOT NULL
        GROUP BY 1
        HAVING COUNT(DISTINCT f.order_id) >= 100
        ORDER BY late_orders DESC
        LIMIT 10;
    """

    try:
        monthly = load_data(monthly_sql)
        states = load_data(state_sql)
        categories = load_data(category_sql)

        if monthly.empty:
            st.info("No delivery trend data is available.")
            return

        monthly["late_delivery_pct"] = pd.to_numeric(monthly["late_delivery_pct"], errors="coerce")
        monthly["delivered_orders"] = pd.to_numeric(monthly["delivered_orders"], errors="coerce")
        states["late_delivery_rate"] = pd.to_numeric(states["late_delivery_rate"], errors="coerce")
        categories["late_delivery_rate"] = pd.to_numeric(categories["late_delivery_rate"], errors="coerce")

        delivered = monthly["delivered_orders"].sum()
        late_rate = (
            (monthly["late_delivery_pct"] * monthly["delivered_orders"]).sum() / delivered
            if delivered else 0
        )
        total_late = (
            monthly["late_delivery_pct"] * monthly["delivered_orders"] / 100
        ).sum()

        a, b = st.columns(2)
        a.metric("Late Delivery Rate", f"{late_rate:.2f}%")
        b.metric("Estimated Late Orders", f"{total_late:,.0f}")

        st.markdown("#### Monthly Late Delivery Trend")
        st.line_chart(
            monthly.set_index("order_month")[["late_delivery_pct"]],
            use_container_width=True
        )

        left, right = st.columns(2)
        with left:
            st.markdown("#### Late Delivery Rate by State")
            st.bar_chart(
                states.sort_values("late_delivery_rate", ascending=False)
                      .head(10).set_index("customer_state")[["late_delivery_rate"]],
                use_container_width=True
            )
        with right:
            st.markdown("#### Late Orders by Product Category")
            st.bar_chart(
                categories.sort_values("late_orders", ascending=False)
                          .head(10).set_index("product_category")[["late_orders"]],
                use_container_width=True
            )

        with st.expander("View state-level delivery data"):
            st.dataframe(states, use_container_width=True, hide_index=True)
        with st.expander("View category-level delivery data"):
            st.dataframe(categories, use_container_width=True, hide_index=True)

    except Exception as error:
        st.error("Delivery analysis data could not be loaded.")
        st.code(str(error))
