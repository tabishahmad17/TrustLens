# TrustLens — AI-Powered E-commerce Analytics

**A Governed AI Analytics Assistant for E-commerce Delivery and Customer Satisfaction**

TrustLens is an end-to-end analytics project built using Python, PostgreSQL, Power BI, and Streamlit. It analyzes e-commerce delivery performance, customer satisfaction, sales trends, and operational issues using business intelligence and AI-assisted SQL analysis.

## Business Problem

Late deliveries can negatively affect customer satisfaction and business performance. TrustLens helps analyze delivery delays, identify operational patterns, and investigate business questions using data.

## Key Features

- **Data Engineering:** Load and process raw e-commerce datasets using Python.
- **Data Quality:** Validate missing values and data consistency.
- **SQL Analytics:** Analyze delivery performance, sales, sellers, products, and customer reviews using PostgreSQL.
- **Power BI Dashboard:** Monitor business KPIs and delivery performance.
- **AI Analytics Assistant:** Ask business questions in natural language and receive SQL-based analysis.
- **Audit Logging:** Maintain a record of assistant queries and execution outcomes.

## Technology Stack

| Area | Technologies |
|---|---|
| Programming | Python |
| Database | PostgreSQL |
| Data Analysis | Pandas, NumPy |
| Visualization | Power BI, Matplotlib |
| AI | Google Gemini |
| SQL Validation | SQLGlot |
| Application | Streamlit |
| Database Connectivity | Psycopg2 |

## Project Structure

```text
TrustLens/
├── app/
│   └── streamlit_app.py
├── data/
│   ├── raw/
│   └── processed/
├── docs/
│   ├── business_brief.md
│   ├── data_dictionary.md
│   └── data_quality_report.md
├── notebook/
│   └── TrustLens_Python_EDA_Local.ipynb
├── powerbi/
├── sql/
├── src/
│   ├── assistant/
│   ├── ingestion/
│   └── validation/
├── tests/
├── .gitignore
└── requirements.txt
```

## Analytics Areas

- Monthly sales and GMV analysis
- Average order value (AOV)
- Late delivery rate
- Customer review analysis
- State-wise delivery performance
- Seller and product category analysis
- Payment and cancellation analysis

## AI Assistant Workflow

1. User submits a business question.
2. Gemini generates an SQL query.
3. SQLGlot validates the generated query.
4. PostgreSQL executes the query.
5. The assistant explains the returned results.
6. The interaction is recorded in the audit log.

## Power BI Dashboard

The project includes two dashboard pages:

- Operations Overview
- Delivery Analysis

These dashboards provide visual monitoring of key business metrics and delivery performance.

## Dataset

The project uses the Brazilian E-Commerce Public Dataset by Olist.

The dataset contains approximately 100,000 orders and multiple related tables covering customers, orders, products, sellers, payments, reviews, and geolocation.

## Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd TrustLens
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure your database connection and Gemini API key using environment variables in a local `.env` file.

Run the Streamlit application:

```bash
streamlit run app/streamlit_app.py
```

**Note:** PostgreSQL must be configured with the required TrustLens database and analytics objects before running the application.

## Security

- Environment secrets are excluded from Git using `.gitignore`.
- SQL validation is applied before query execution.
- Database query execution uses read-only session settings.
- Assistant interactions are logged for auditing.

## Project Objective

The objective of TrustLens is to demonstrate how data engineering, business intelligence, SQL analytics, and generative AI can work together to support data-driven business decisions.

---

**Project:** TrustLens  
**Focus:** Data Analytics | Business Intelligence | AI-Assisted SQL Analytics