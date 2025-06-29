import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

# File paths
input_file = "/opt/airflow/data/transformed_data/depmap_clean.csv"
output_file = "/opt/airflow/data/alerts/mutation_alerts.csv"
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Read input CSV
df = pd.read_csv(input_file, low_memory=False)

# Function to label mutations
def label_mutation(row):
    if row.get("isdeleterious"):
        return "DELETERIOUS"
    elif row.get("istcgahotspot"):
        return "HOTSPOT"
    elif row.get("hugo_symbol") in ["BRCA1", "BRCA2", "TP53", "EGFR", "PIK3CA"]:
        return "KNOWN_GENE"
    return None

# Apply mutation flagging
df["mutation_flag"] = df.apply(label_mutation, axis=1)

# Filter alerts and save to CSV
alerts = df[df["mutation_flag"].notnull()]
alerts.to_csv(output_file, index=False)
print(f"Saved {len(alerts)} alerts with flags to {output_file}")

# Load environment variables
load_dotenv()

# Database connection parameters
db_params = {
    "host": os.getenv("POSTGRES_HOST", "postgres"),
    "dbname": os.getenv("POSTGRES_DB", "mutations"),
    "user": os.getenv("POSTGRES_USER", "airflow"),
    "password": os.getenv("POSTGRES_PASSWORD", "airflow"),
    "port": os.getenv("POSTGRES_PORT", "5432")
}

# Connect to PostgreSQL
conn = psycopg2.connect(**db_params)
cur = conn.cursor()

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

# Convert value to boolean
def to_bool(val):
    if pd.isna(val):
        return False
    return bool(val)

# Insert alerts into PostgreSQL
for _, row in alerts.iterrows():
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

# Commit and close the connection
conn.commit()
cur.close()
conn.close()
print("Mutation flags stored in PostgreSQL.")
