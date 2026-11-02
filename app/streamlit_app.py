

import sys
from pathlib import Path

import streamlit as st

# --------------------------------------------------
# PROJECT PATH
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ASSISTANT_PATH = PROJECT_ROOT / "src" / "assistant"

sys.path.insert(0, str(ASSISTANT_PATH))

from chat_router import route_message
from dashboard import render_operations_dashboard, render_delivery_analysis


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="TrustLens AI Assistant",
    page_icon="🔍",
    layout="wide"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>
:root { --ink:#17243b; --muted:#64748b; --page:#f4f7fc; }
.stApp,[data-testid="stAppViewContainer"]{background:var(--page);color:var(--ink)}
[data-testid="stHeader"]{background:rgba(244,247,252,.92)}
.block-container{max-width:1440px;padding-top:2rem;padding-bottom:3rem}
[data-testid="stSidebar"]{background:#14233f;border-right:1px solid #263b60}
[data-testid="stSidebar"] *{color:#edf3ff !important}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p{color:#c8d5ec !important}
[data-testid="stSidebar"] [role="radiogroup"] label{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.09);border-radius:10px;padding:.55rem .7rem;margin-bottom:.35rem}
[data-testid="stSidebar"] [role="radiogroup"] label:hover{background:rgba(255,255,255,.13)}
.hero-panel{background:linear-gradient(115deg,#172b50 0%,#3157a4 65%,#5277bf 100%);border-radius:20px;padding:1.7rem 2rem;color:white;margin:.25rem 0 1.5rem;box-shadow:0 12px 30px rgba(34,62,110,.14)}
.hero-panel h1,.hero-panel p,.hero-panel span{color:white !important}
.hero-kicker{text-transform:uppercase;letter-spacing:.12em;font-size:.75rem;opacity:.82;font-weight:700}
.hero-panel h1{font-size:2.1rem;margin:.35rem 0 .45rem}
.hero-panel p{font-size:1rem;margin:0;opacity:.9}
.section-heading{color:#17243b;font-weight:700;font-size:1.2rem;margin:1.2rem 0 .75rem}
.feature-card{background:white;border:1px solid #e4eaf3;border-radius:15px;padding:1rem 1.1rem;min-height:112px;box-shadow:0 4px 14px rgba(31,52,86,.04)}
.feature-card .feature-title{color:#1e3152;font-weight:700;margin-bottom:.35rem}
.feature-card .feature-copy{color:#64748b;font-size:.9rem}
[data-testid="stMetric"]{background:white;border:1px solid #e4eaf3;border-radius:14px;padding:1rem 1.1rem;box-shadow:0 4px 14px rgba(31,52,86,.04)}
[data-testid="stMetricLabel"]{color:#64748b !important}
[data-testid="stMetricValue"]{color:#17243b !important}
[data-testid="stChatMessage"]{background:white;border:1px solid #e4eaf3;border-radius:14px;padding:.9rem 1rem}
[data-testid="stChatInput"]{border-radius:14px}
h1,h2,h3{color:#17243b}
[data-testid="stCaptionContainer"]{color:#64748b}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# PAGE NAVIGATION
# --------------------------------------------------

page = st.sidebar.radio(
    "Navigate",
    ["Operations Overview", "Delivery Analysis", "AI Assistant"]
)

if page == "Operations Overview":
    st.title("🔍 TrustLens")
    st.write("Explore e-commerce performance through interactive analytics.")
    render_operations_dashboard()
    st.stop()

if page == "Delivery Analysis":
    st.title("🔍 TrustLens")
    st.write("Explore delivery performance, delays and customer impact.")
    render_delivery_analysis()
    st.stop()


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.markdown(
        '<div style="font-size:1.55rem;font-weight:800;color:#ffffff !important;">🔍 TrustLens</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div style="font-size:0.84rem;color:#c8d5ec !important;line-height:1.5;">Governed E-commerce Analytics</div>',
        unsafe_allow_html=True
    )
    st.divider()
    st.markdown("**Explore your workspace**")
    st.caption("Choose a section above to explore performance or ask business questions.")
    st.divider()
    st.markdown("**AI assistant can help with**")
    st.markdown("""
    **💬 General Chat**
    - General business questions

    **📘 SQL Learning**
    - Joins, CTEs and aggregations
    - Interview preparation

    **📊 Business Analytics**
    - Revenue and orders
    - Delivery delays
    - Customer satisfaction
    - Seller performance
    """)
    st.divider()
    st.caption("Powered by Gemini · PostgreSQL")
    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# --------------------------------------------------
# MAIN HEADER
# --------------------------------------------------

st.markdown("""
<div class="hero-panel">
  <div class="hero-kicker">Your e-commerce intelligence workspace</div>
  <h1>TrustLens AI Assistant</h1>
  <p>Ask questions, explore business performance and turn your data into clear decisions.</p>
</div>
""", unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown('<div class="section-heading">What would you like to explore?</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="feature-card"><div class="feature-title">📦 Orders & Revenue</div><div class="feature-copy">Explore GMV, order volume and monthly business trends.</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="feature-card"><div class="feature-title">🚚 Delivery Performance</div><div class="feature-copy">Investigate late deliveries, regions and product categories.</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="feature-card"><div class="feature-title">⭐ Customer Satisfaction</div><div class="feature-copy">Understand review scores and customer experience patterns.</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Try asking</div>', unsafe_allow_html=True)
    p1, p2 = st.columns(2)
    with p1:
        st.markdown("- Which states have the highest late-delivery rate?\n- Show monthly GMV and order trends.")
    with p2:
        st.markdown("- How do delivery delays relate to review scores?\n- Which product categories have the most late orders?")
else:
    st.markdown('<div class="section-heading">Conversation</div>', unsafe_allow_html=True)

st.divider()


# --------------------------------------------------
# DISPLAY CHAT HISTORY
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message.get("sql"):

            with st.expander("View Generated SQL"):
                st.code(message["sql"], language="sql")

        if message.get("rows") is not None:

            with st.expander("View Database Results"):

                if message["rows"]:
                    st.dataframe(
                        message["rows"],
                        use_container_width=True
                    )
                else:
                    st.info("The query returned no rows.")


# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------

question = st.chat_input("Ask TrustLens anything...")


# --------------------------------------------------
# PROCESS USER QUESTION
# --------------------------------------------------

if question:

    with st.chat_message("user"):
        st.markdown(question)

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("assistant"):

        with st.spinner("TrustLens is thinking..."):

            try:

                result = route_message(question)

                response_type = result.get("type", "general")

                answer = result.get("answer")

                if not answer:
                    answer = "I could not generate an answer. Please try again."

                st.markdown(answer)

                # Display generated SQL
                sql = result.get("sql")

                if sql:
                    with st.expander("View Generated SQL"):
                        st.code(sql, language="sql")

                # Display database results
                rows = result.get("rows")

                if rows is not None:

                    with st.expander("View Database Results"):

                        if rows:
                            st.dataframe(
                                rows,
                                use_container_width=True
                            )
                        else:
                            st.info("The query returned no rows.")

                # Save assistant response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "type": response_type,
                    "sql": sql,
                    "rows": rows
                })

            except Exception as error:

                error_message = str(error)

                if (
                    "429" in error_message
                    or "RESOURCE_EXHAUSTED" in error_message
                ):

                    answer = (
                        "Gemini's free-tier daily quota has been reached. "
                        "Please try again after the quota resets. "
                        "No billing is required."
                    )

                else:

                    answer = (
                        "Something went wrong while processing your request. "
                        "Please try again."
                    )

                st.error(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })
