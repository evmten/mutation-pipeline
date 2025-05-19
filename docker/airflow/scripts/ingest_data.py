import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import pandas as pd
import re

load_dotenv()  # Load variables from .env

# === CONFIG ===
conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
container_name = "raw"
download_folder = "/opt/airflow/data/ingested_data/"
os.makedirs(download_folder, exist_ok=True)

# Files to fetch
files_to_download = [
    "data.csv",
    "brca_data_w_subtypes.csv",
    "CCLE_mutations.csv",
    "Glioblastoma Multiforme Dead - Sheet1.csv"
]

# === Azure Client ===
blob_service = BlobServiceClient.from_connection_string(conn_str)
container_client = blob_service.get_container_client(container_name)

def normalize_filename(name):
    base, ext = os.path.splitext(name)  # Splits "file.csv" -> ("file", ".csv")
    base = re.sub(r"[^a-z0-9_]", "_", base.lower().replace(" ", "_"))
    return base + ext  # Reattach the original extension

# === Download Loop ===
for filename in files_to_download:
    try:
        blob_client = container_client.get_blob_client(filename)
        local_filename  = normalize_filename(filename)
        download_path = os.path.join(download_folder, local_filename)

        with open(download_path, "wb") as f:
            stream = blob_client.download_blob()
            f.write(stream.readall())
            print(f"Downloaded: {local_filename}")

        # === Basic Validation ===
        try:
            df = pd.read_csv(download_path, low_memory=False)
            print(f"{local_filename} loaded: shape = {df.shape}, missing values = {df.isnull().sum().sum()}")
        except Exception as e:
            print(f"Failed to validate {local_filename}: {e}")

    except Exception as e:
        print(f"Error processing {local_filename}: {e}")