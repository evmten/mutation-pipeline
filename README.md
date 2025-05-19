# 🧬 Mutation Analysis Data Pipeline

This project is a **bioinformatics-inspired data engineering pipeline** that identifies potentially harmful gene mutations. It is designed as a modular system with **data ingestion, transformation, mutation flagging, and dashboard visualization**, orchestrated through **Apache Airflow** and supported by a **PostgreSQL database** and a **Streamlit dashboard**.

---

## 📌 Features

- **Automated ETL pipeline** using Apache Airflow
- **Mutation analysis logic** to flag deleterious variants
- **PostgreSQL database** for storing alerts
- **Streamlit dashboard** for interactive exploration
- Fully containerized with **Docker**
- Basic testing and logging included

---

## 📁 Project Structure

mutation-pipeline/
│
├── docker/
│ └── airflow/ # Airflow setup (Dockerfile, dags/, etc.)
│
├── src/
│ ├── ingestion/ # Simulated ingestion or batch download
│ ├── transformation/ # Filtering and mutation processing
│ ├── analysis/ # Flagging harmful mutations
│ └── validation/ # Optional data validation scripts
│
├── dags/
│ ├── ingest_dag.py
│ ├── analyze_dag.py
│ └── validate_dag.py
│
├── data/
│ ├── raw/ # Input data files (e.g. ccle_mutations.csv)
│ ├── processed_data/ # Cleaned mutation datasets
│ └── alerts/ # Mutation alerts (CSV or pushed to DB)
│
├── streamlit_app/
│ └── app.py # Streamlit dashboard
│
├── requirements.txt
├── docker-compose.yml
└── README.md
---

## 🔄 Pipeline Overview

### 1. **Ingestion**
- Loads mutation data from local files (e.g. `ccle_mutations.csv`)
- Scheduled and managed via Airflow (`ingest_dag.py`)

### 2. **Transformation**
- Filters relevant columns (e.g. `Hugo_Symbol`, `Variant_Type`, `isDeleterious`)
- Cleans and prepares the dataset for analysis

### 3. **Mutation Analysis**
- Applies rule-based logic to flag potentially harmful mutations
- Outputs a mutation alert CSV and stores it in PostgreSQL

### 4. **Dashboard**
- Streamlit app allows users to:
  - Explore flagged mutations
  - Filter by gene, mutation type, etc.
  - View alert statistics

---

## 🛠 Technologies Used

| Tool         | Purpose                           |
|--------------|-----------------------------------|
| Python       | Core scripting and logic          |
| Apache Airflow | Workflow orchestration          |
| PostgreSQL   | Database for alert storage        |
| Streamlit    | Dashboard and frontend            |
| Docker       | Containerization of all services  |
| Pandas       | Data manipulation and filtering   |
| GitHub Actions (optional) | CI/CD automation    |

---

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose installed
- Basic familiarity with Airflow and Python

### Quickstart

```bash
# Clone the repo
git clone https://github.com/evmten/mutation-pipeline.git
cd mutation-pipeline

# Start the pipeline
docker-compose up --build

Then:

Visit Airflow: http://localhost:8080

Visit Streamlit Dashboard: http://localhost:8501

🧪 Example Use Case
This pipeline could be adapted for:

Flagging mutations in cancer-related datasets

Running nightly mutation scans on fresh genomic data

Integrating with external APIs or research dashboards

🧼 Future Improvements
Add more complex mutation-scoring logic

Expand the dashboard to show mutation pathways or gene interactions

Integrate with real-time genomics APIs (e.g., COSMIC, Ensembl)

Include advanced alerting (e.g., email or Slack)
