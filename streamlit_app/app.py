import os
import pandas as pd
import psycopg2
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connect to the PostgreSQL db
try:
    db_params = {
        "host": os.getenv("POSTGRES_HOST", "localhost"),  # Change to 'postgres' if inside Docker
        "dbname": os.getenv("POSTGRES_DB", "mutations"),
        "user": os.getenv("POSTGRES_USER", "airflow"),
        "password": os.getenv("POSTGRES_PASSWORD", "airflow"),
        "port": os.getenv("POSTGRES_PORT", "5432")
    }
    conn = psycopg2.connect(**db_params)
except psycopg2.OperationalError as e:
    st.error(f"Database connection failed:\n{e}")
    st.stop()

# Query the data from the mutation_flags table
try:
    query = "SELECT * FROM mutation_flags"
    df = pd.read_sql(query, conn)
    conn.close()
except Exception as e:
    st.error(f"Failed to load data: {e}")
    st.stop()

# Streamlit Dashboard Title
st.title("Mutation Alert Dashboard")

# Filters
flag_filter = st.multiselect("Filter by Mutation Flag", df["mutation_flag"].unique())
gene_filter = st.text_input("Filter by Hugo Symbol (gene)")

# Apply filters to the dataframe
filtered_df = df.copy()
if flag_filter:
    filtered_df = filtered_df[filtered_df["mutation_flag"].isin(flag_filter)]
if gene_filter:
    filtered_df = filtered_df[filtered_df["hugo_symbol"].str.contains(gene_filter, case=False, na=False)]

# Display Summary
MAX_CELLS = 100_000
total_cells = filtered_df.shape[0] * filtered_df.shape[1]

st.markdown(f"### Summary")
st.write(f"Unique genes: {filtered_df['hugo_symbol'].nunique()}")
st.write(f"Deleterious mutations: {filtered_df['is_deleterious'].sum()}")
st.write(f"Showing {len(filtered_df)} rows, {total_cells:,} cells")

# Display table with conditional styling
if total_cells > MAX_CELLS:
    st.warning("Too many cells to apply styling. Showing plain table.")
    st.dataframe(filtered_df)
else:
    def highlight_flags(val):
        return 'background-color: salmon' if val else ''
    st.dataframe(filtered_df.style.applymap(highlight_flags, subset=["mutation_flag"]))
