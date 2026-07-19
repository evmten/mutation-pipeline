# Genomic Mutation Data Pipeline

This project is a **bioinformatics-inspired data engineering pipeline** that identifies potentially harmful gene mutations. It is designed as a modular system with **data ingestion, transformation, mutation flagging, and dashboard visualization**, orchestrated through **Apache Airflow** and supported by a **PostgreSQL database** and a **Streamlit dashboard**.

---

## Features

- **Orchestrated ETL pipeline** using Apache Airflow
- **Mutation analysis logic** to flag deleterious variants
- **PostgreSQL database** for storing alerts
- **Streamlit dashboard** for interactive exploration
- Fully containerized with **Docker**
- Basic logging and validation included

## Data sources

- **CCLE mutations** (`CCLE_mutations.csv`) — Cancer Cell Line Encyclopedia,
  from the Broad Institute's DepMap portal. This is the dataset the analysis
  runs on. (Confirmed by the columns the pipeline selects: DepMap_ID,
  isDeleterious, isTCGAhotspot, Genome_Change, ExAC_AF.)
- **Additional datasets, ingested and cleaned but not analysed:** a
  breast-cancer dataset with molecular subtypes (`brca_data_w_subtypes.csv`)
  and a glioblastoma clinical/survival dataset (`Glioblastoma Multiforme Dead - Sheet1.csv`,
  originally an Excel export). These were staged during development; only the
  CCLE file is carried through to flagging and the dashboard.

  Raw files were stored in an Azure Blob container as a cloud landing zone.
  The CCLE file is publicly available from DepMap.

## Pipeline Overview

### 1. **Ingestion**
- Ingests mutation datasets from Azure Blob Storage via Airflow (`ingest_dag.py`), with basic shape and missing-value validation on download

### 2. **Transformation**
- Cleans column names to consistent snake_case across all datasets
- Narrows the CCLE file to the relevant columns (e.g. `Hugo_Symbol`, `Variant_Type`, `isDeleterious`)

### 3. **Mutation Analysis**
- Applies rule-based logic to flag potentially harmful mutations
- Outputs a mutation alert CSV and stores it in PostgreSQL

### 4. **Dashboard**
- Streamlit app allows users to:
  - Explore flagged mutations
  - Filter by gene, mutation type, etc.
  - View alert statistics

---

## Technologies Used

| Tool         | Purpose                           |
|--------------|-----------------------------------|
| Python       | Core scripting and logic          |
| Apache Airflow | Workflow orchestration          |
| Azure Blob Storage | Cloud storage and data ingestion source |
| PostgreSQL   | Database for alert storage        |
| Streamlit    | Dashboard and frontend            |
| Docker       | Containerization of all services  |
| Pandas       | Data manipulation and filtering   |

---

## Getting Started

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
```
#### Then:
- Visit Airflow: http://localhost:8080

- Visit Streamlit Dashboard: http://localhost:8501

#### Example Use Case
This pipeline could be adapted for:

- Flagging mutations in cancer-related datasets

- Running nightly mutation scans on fresh genomic data

- Integrating with external APIs or research dashboards

#### Future Improvements
- Add more complex mutation-scoring logic

- Expand the dashboard to show mutation pathways or gene interactions

- Integrate with real-time genomics APIs (e.g., COSMIC, Ensembl)

- Include advanced alerting (e.g., email or Slack)
