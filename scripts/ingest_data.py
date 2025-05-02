import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env

# === CONFIG ===
conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
container_name = "raw"
download_folder = "data/ingested_data/"
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

# === Download Loop ===
for filename in files_to_download:
    blob_client = container_client.get_blob_client(filename)
    download_path = os.path.join(download_folder, filename)

    with open(download_path, "wb") as f:
        stream = blob_client.download_blob()
        f.write(stream.readall())
        print(f"Downloaded: {filename}")
