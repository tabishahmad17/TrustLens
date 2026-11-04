# 🔎 TrustLens — Governed AI Analytics for E-commerce

<p align="center">
  <strong>Explore delivery performance, customer satisfaction and e-commerce operations with PostgreSQL, Power BI and a Gemini-powered analytics assistant.</strong>
</p>

<p align="center">
  <a href="https://trustlens-u7stusobuiarm6jzslqsyu.streamlit.app/"><strong>🚀 Open the Live Application</strong></a>
  &nbsp; · &nbsp;
  <a href="https://github.com/tabishahmad17/TrustLens"><strong>View Source Code</strong></a>
</p>

<p align="center">
  <img src="screenshots/Screenshot%202026-11-02%20230201.png" alt="TrustLens Operations Overview dashboard" width="92%">
</p>

---

## 1. Project Overview

**TrustLens** is an end-to-end e-commerce analytics project built around the Brazilian E-Commerce Public Dataset by Olist. It brings together data preparation, PostgreSQL analytics, Power BI reporting and a natural-language AI assistant.

The project focuses on understanding order performance, gross merchandise value (GMV), delivery delays and customer review patterns. The Streamlit application provides an Operations Overview, Delivery Analysis and an AI Assistant that can answer business questions using database-backed SQL queries.

> **Important:** TrustLens analyzes historical data and observed relationships. It does not predict or prevent delivery delays, and correlation should not be interpreted as causation.

## 2. Live Demo

**[Launch TrustLens on Streamlit Community Cloud](https://trustlens-u7stusobuiarm6jzslqsyu.streamlit.app/)**

The live application connects to a hosted PostgreSQL database on Neon. Availability of AI responses also depends on the configured Gemini API key and API quota.

## 3. Features

### Operations Overview
- Total orders, GMV, late-delivery rate and average review score.
- Monthly revenue and order trends.
- Monthly delivery performance and state-level comparisons.

### Delivery Analysis
- Selectable purchase-date range.
- Late-delivery rate, average actual delivery days and average estimated delivery days.
- Review-score comparison by delay bucket.
- Product categories with higher late-delivery rates.
- Monthly actual-versus-estimated delivery days.
- State-level delivery summary.

### TrustLens AI Assistant
- Ask business questions in natural language.
- Generate SQL with Google Gemini using the project schema context.
- Validate generated SQL before execution.
- Display generated SQL and database results.
- Provide a business-oriented explanation of results.
- Record assistant activity in a PostgreSQL audit table.

### Data and governance
- Python-based data preparation and quality checks.
- Raw and analytics schemas in PostgreSQL.
- Reusable analytics views and SQL analysis scripts.
- Separate database roles for read-only analytics and audit logging.
- Query validation, read-only transaction settings, a query timeout and a result-row cap.

## 4. Application Screenshots

### Operations Overview
![TrustLens Operations Overview](screenshots/Screenshot%202026-11-02%20230201.png)

### Delivery Analysis
![TrustLens Delivery Analysis](screenshots/Screenshot%202026-11-02%20230219.png)

### AI Assistant
![TrustLens AI Assistant](screenshots/Screenshot%202026-11-02%20230317.png)

### Generated SQL and database results
![TrustLens SQL generation and results](screenshots/Screenshot%202026-11-02%20230518.png)

## 5. Architecture

~~~mermaid
flowchart TD
    A["Olist e-commerce dataset"] --> B["Python data preparation and validation"]
    B --> C[("PostgreSQL on Neon")]
    C --> D["Raw and analytics schemas"]
    D --> E["Analytics views and SQL"]
    E --> F["Power BI dashboards"]
    D --> G["Streamlit application"]
    G --> H["Natural-language question"]
    H --> I["Google Gemini"]
    I --> J["SQL generation"]
    J --> K["SQLGlot validation"]
    K --> L["Read-only PostgreSQL query execution"]
    L --> M["Results and explanation"]
    L --> N["Audit logging"]
~~~

**Application flow:** Python prepares and validates the data; PostgreSQL stores the raw and analytics data; Power BI presents business dashboards; and the Streamlit assistant uses Gemini to help translate business questions into validated SQL.

## 6. Technology Stack

| Area | Tools |
|---|---|
| Programming | Python |
| Data preparation | Pandas, NumPy |
| Database | PostgreSQL, Neon |
| Business intelligence | Power BI |
| Web application | Streamlit |
| Generative AI | Google Gemini (gemini-2.5-flash) |
| SQL parsing and validation | SQLGlot |
| Database connectivity | Psycopg2 |
| Local configuration | python-dotenv |
| Analysis and exploration | Jupyter Notebook, Matplotlib |

## 7. Dataset

TrustLens uses the **Brazilian E-Commerce Public Dataset by Olist**. It contains approximately 100,000 orders and related data about customers, geolocation, order items, payments, reviews, products, sellers and product-category translations.

The project’s raw schema contains these nine source tables:

- customers
- geolocation
- order_items
- order_payments
- order_reviews
- orders
- products
- sellers
- category_translation

The analytics schema contains reusable views used by the dashboards and assistant, including **v_monthly_kpis**, **v_order_facts** and **v_seller_performance**.

## 13. Repository Structure

~~~text
TrustLens/
├── app/
│   ├── streamlit_app.py
│   └── dashboard.py
├── data/
│   ├── raw/                 # Source data (not committed)
│   └── processed/           # Processed files (not committed)
├── docs/
│   ├── business_brief.md
│   ├── data_dictionary.md
│   └── data_quality_report.md
├── notebook/
│   └── TrustLens_Python_EDA_Local.ipynb
├── powerbi/                 # Power BI project files
├── screenshots/             # README application screenshots
├── sql/
│   ├── 01_data_quality.sql
│   ├── 02_delivery_analysis.sql
│   ├── 03_customer_satisfaction.sql
│   ├── 04_business_analysis.sql
│   ├── 05_read_only_user.sql
│   └── 06_audit_user.sql
├── src/
│   └── assistant/            # AI, database, SQL validation and audit modules
├── tests/
├── .gitignore
├── README.md
└── requirements.txt
~~~

## 14. Run Locally

### Prerequisites
- Python 3.10 or later.
- PostgreSQL database with the TrustLens raw tables, analytics views and audit table configured.
- A Google Gemini API key.
- Git.

### 1. Clone the repository

~~~bash
git clone https://github.com/tabishahmad17/TrustLens.git
cd TrustLens
~~~

### 2. Create and activate a virtual environment

**Windows PowerShell:**

~~~powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
~~~

**macOS / Linux:**

~~~bash
python -m venv .venv
source .venv/bin/activate
~~~

### 3. Install dependencies

~~~bash
pip install -r requirements.txt
~~~

### 4. Configure environment variables

Create a **.env** file in the repository root. Add your own values locally; **never commit this file or share its contents**.

~~~dotenv
GEMINI_API_KEY=your_gemini_api_key

DB_HOST=your_postgres_host
DB_PORT=5432
DB_NAME=your_database_name
DB_SSLMODE=require

DB_READER_USER=trustlens_reader
DB_READER_PASSWORD=your_reader_password

DB_AUDIT_USER=trustlens_auditor
DB_AUDIT_PASSWORD=your_auditor_password

# Optional: administrator credentials for database setup tasks only
DB_USER=your_admin_username
DB_PASSWORD=your_admin_password
~~~

The application reads configuration from environment variables / the local .env file, or from Streamlit secrets when deployed. Use separate, least-privilege credentials for the reader and auditor roles. Do not use the database-owner account for routine analytics queries.

### 5. Prepare the database

Create/configure the PostgreSQL database and load the Olist source tables into the **raw** schema. Create the analytics views and the **ops.audit_log** table required by the application.

The SQL scripts in **sql/** document the data-quality checks, delivery analysis, customer-satisfaction analysis, business analysis and database-role grants. Review each script and run it with an appropriately privileged database account in the intended order. The role scripts create roles and grant permissions; configure each role's password separately and securely.

### 6. Start the Streamlit application

~~~bash
streamlit run app/streamlit_app.py
~~~

Open the local URL printed by Streamlit in your browser.

## 15. Streamlit Community Cloud Deployment

The deployed application is hosted at:

**[https://trustlens-u7stusobuiarm6jzslqsyu.streamlit.app/](https://trustlens-u7stusobuiarm6jzslqsyu.streamlit.app/)**

For deployment, configure the same required keys from the .env example in the app's **Streamlit Cloud → Settings → Secrets** section using TOML format:

~~~toml
GEMINI_API_KEY = "your_gemini_api_key"

DB_HOST = "your_postgres_host"
DB_PORT = "5432"
DB_NAME = "your_database_name"
DB_SSLMODE = "require"

DB_READER_USER = "trustlens_reader"
DB_READER_PASSWORD = "your_reader_password"

DB_AUDIT_USER = "trustlens_auditor"
DB_AUDIT_PASSWORD = "your_auditor_password"
~~~

Only add **DB_USER** and **DB_PASSWORD** if the deployed application setup path requires the administrator connection. Never put secrets in source code, screenshots, README values or Git history.

## 16. Database Security and Governance

TrustLens separates database responsibilities:

| Role | Intended responsibility |
|---|---|
| neondb_owner | Database administration and setup |
| trustlens_reader | Read-only analytics queries |
| trustlens_auditor | Insert audit-log records |

The assistant query path includes SQL validation, a read-only database transaction, a 10-second statement timeout and a maximum of 100 returned rows. Audit logging uses a separate database connection.

The reader and auditor permissions were manually checked against the Neon database during project verification. The reader successfully queried the orders table and was denied a DELETE operation. The auditor was denied SELECT access to the audit table; an INSERT test was run inside a transaction and rolled back.

These checks verify the tested database-role behavior; they are not a full security audit or a guarantee that every application path is vulnerability-free.

## 17. Limitations

- The analysis is based on historical Olist e-commerce data.
- Observed relationships do not establish causation.
- AI-generated SQL and explanations depend on the model, schema context, database availability and configured API quota.
- Results depend on the selected date range and the definitions used in the SQL measures.
- The application is an analytics and investigation tool; it does not predict or prevent delivery delays.

## 18. Future Improvements

- Expand automated tests for SQL validation, query execution and database permissions.
- Add monitoring for application errors and database availability.
- Continue refining documentation and reproducible database setup.
- Evaluate additional business questions and analytical measures.

---

## Project Information

- **Project:** TrustLens
- **Domain:** E-commerce analytics
- **Focus:** Data analytics · PostgreSQL · Power BI · Generative AI · Data governance
- **Live demo:** [TrustLens on Streamlit](https://trustlens-u7stusobuiarm6jzslqsyu.streamlit.app/)
- **Repository:** [tabishahmad17/TrustLens](https://github.com/tabishahmad17/TrustLens)


## 8. KPI Definitions

The following definitions describe the measures used in the project. Always apply the same date filters and denominator when comparing Power BI, PostgreSQL and Streamlit results.

| KPI | Project definition |
|---|---|
| GMV | Sum of order-item prices. Freight is not included in this item-price definition. |

**Displayed Operations Overview GMV:** approximately **₹13.5M (₹1,35,00,000 / 1 crore 35 lakh)**. This is the rounded value shown on the dashboard; use the underlying exact database measure for precise reporting.
| Total Orders | Count of distinct order IDs in the selected scope. |
| Average Order Value (AOV) | GMV divided by total orders, using the same order population and filters. |
| Late Delivery Rate | Late delivered orders divided by delivered orders, expressed as a percentage. A delivery is late when its actual delivery date is later than its estimated delivery date. |
| Average Review Score | Average of available review scores in the selected population. |

**Data-quality note:** The data-quality report identifies eight delivered orders with missing actual delivery dates. Such orders cannot be classified reliably as early, on-time or late from the available dates. Check how the selected query/view handles these records before comparing late-delivery rates across tools.

## 9. Verified Data-Quality Findings

The checks documented in this repository identified:
- Eight delivered orders with missing actual delivery dates.
- One delivered order with no matching payment record.
- Nine source tables loaded into the raw schema, with the row counts documented in [the data-quality report](docs/data_quality_report.md).

These are data-quality findings, not claims that a particular operational factor caused late deliveries or lower review scores.

## 10. Tests and Verification

The repository contains manual smoke-test scripts under `tests/`. They are not currently a complete automated `pytest` test suite.

For the SQL-validator script, run from the repository root:

**Windows PowerShell**
```powershell
$env:PYTHONPATH = "src/assistant"
python tests/test_sql_validator.py
```

**macOS / Linux**
```bash
PYTHONPATH=src/assistant python tests/test_sql_validator.py
```

Database-connection and query-runner scripts require valid local environment configuration and access to the configured PostgreSQL database. Run them only after setting up the database credentials. Do not commit your local `.env` file.

Manual database-role checks are described in the security section above. They do not replace automated tests or a professional security audit.

## 11. Dataset Source and Usage

The source dataset is the [Brazilian E-Commerce Public Dataset by Olist on Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce). The source data covers orders from 2016–2018.

Review the dataset's current Kaggle terms and license before redistributing source data or a Power BI `.pbix` file that may contain an imported copy of the data. This repository does not make a separate claim that redistribution rights have been granted.

## 12. Live Application Availability

The live demo is hosted on Streamlit Community Cloud. On a free hosting tier, an app that has been inactive may take a little time to wake up when first opened. AI responses also depend on Gemini API availability and quota.
