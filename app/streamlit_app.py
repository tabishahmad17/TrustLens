

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
from dashboard import render_dashboard


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

.main {
    background-color: #f5f7fb;
}

.block-container {
    padding-top: 2rem;
    max-width: 1100px;
}

.stChatMessage {
    border-radius: 12px;
}

.sidebar-title {
    font-size: 24px;
    font-weight: bold;
    color: #ffffff;
}

.sidebar-text {
    color: #d0d7e2;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# PAGE NAVIGATION
# --------------------------------------------------

page = st.sidebar.radio(
    "Navigate",
    ["Operations Dashboard", "AI Assistant"]
)

if page == "Operations Dashboard":
    st.title("🔍 TrustLens")
    st.write("Explore e-commerce performance through interactive analytics.")
    render_dashboard()
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
        '<div class="sidebar-title">🔍 TrustLens AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-text">'
        'Your Governed E-commerce Analytics Assistant'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.subheader("What can I help with?")

    st.markdown("""
    **💬 General Chat**
    - Greetings
    - General questions

    **📘 SQL Learning**
    - WHERE vs HAVING
    - Joins and CTEs
    - SQL interview preparation

    **📊 Business Analytics**
    - Revenue and orders
    - Late deliveries
    - Customer satisfaction
    - Seller performance
    """)

    st.divider()

    st.caption("Powered by Gemini + PostgreSQL")

    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# --------------------------------------------------
# MAIN HEADER
# --------------------------------------------------

st.title("TrustLens AI Assistant")

st.write(
    "Ask questions about your e-commerce business, "
    "learn SQL concepts, or have a general conversation."
)

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
