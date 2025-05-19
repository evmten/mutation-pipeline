import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# PostgreSQL connection parameters
db_params = {
    "host": os.getenv("POSTGRES_HOST", "postgres"),
    "dbname": os.getenv("POSTGRES_DB", "mutations"),
    "user": os.getenv("POSTGRES_USER", "airflow"),
    "password": os.getenv("POSTGRES_PASSWORD", "airflow"),
    "port": os.getenv("POSTGRES_PORT", "5432")
}

# CSV with mutation flags
input_path = "/opt/airflow/data/alerts/mutation_alerts.csv"

# Read data
df = pd.read_csv(input_path)

# Optional: limit size if you're testing
# df = df.head(100)

# Connect to PostgreSQL and insert
conn = psycopg2.connect(**db_params)
cur = conn.cursor()

def to_bool(val):
    if pd.isna(val):
        return False
    return bool(val)

# Create table if not exists
cur.execute("""
    CREATE TABLE IF NOT EXISTS mutation_flags (
        id SERIAL PRIMARY KEY,
        hugo_symbol TEXT,
        variant_classification TEXT,
        variant_type TEXT,
        depmap_id TEXT,
        is_deleterious BOOLEAN,
        is_tcga_hotspot BOOLEAN,
        exac_af FLOAT,
        mutation_flag TEXT
    );
""")

# Insert data row-by-row (bulk load can be added later if needed)
for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO mutation_flags (
            hugo_symbol, variant_classification, variant_type, depmap_id,
            is_deleterious, is_tcga_hotspot, exac_af, mutation_flag
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        row.get("hugo_symbol"),
        row.get("variant_classification"),
        row.get("variant_type"),
        row.get("depmap_id"),
        to_bool(row.get("isdeleterious")),
        to_bool(row.get("istcgahotspot")),
        row.get("exac_af"),
        row.get("mutation_flag")
    ))

conn.commit()
cur.close()
conn.close()

print("Mutation flags stored in PostgreSQL.")
