import pandas as pd
import streamlit as st

from query_runner import execute_query


def load_data(sql):
    result = execute_query(sql)
    if not result.get("success"):
        raise RuntimeError(result.get("error", "Unknown database query error."))
    return pd.DataFrame(result.get("rows", []))


def render_dashboard():
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

        a, b, c, d = st.columns(4)
        a.metric("Total Orders", f"{orders:,.0f}")
        b.metric("Total GMV", f"₹{revenue:,.0f}")
        c.metric("Late Delivery Rate", f"{late_rate:.2f}%")
        d.metric("Average Review Score", f"{review:.2f}/5" if pd.notna(review) else "N/A")

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
        st.error("Dashboard data could not be loaded. The diagnostic message is shown below.")
        st.code(str(error))
