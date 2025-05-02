import os
import requests
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env


# === CONFIG ===
conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
container_name = "raw"
local_raw_folder = "data/raw_data/"
files_to_upload = [
    "data.csv",             # Your main BRCA dataset
    "brca_data_w_subtypes.csv",  # BRCA with subtypes
    "Glioblastoma Multiforme Dead - Sheet1.csv",         # Glioblastoma Multiforme
    "CCLE_mutations.csv"
]
# depmap_url = "https://depmap.org/portal/download/api/download?file_name=CCLE_mutations.csv"

# # === Download DepMap if not already there ===
# ccle_path = os.path.join(local_raw_folder, "CCLE_mutations.csv")
# if not os.path.exists(ccle_path):
#     print("Downloading DepMap file...")
#     response = requests.get(depmap_url)
#     with open(ccle_path, "wb") as f:
#         f.write(response.content)
#     print("Downloaded and saved to raw_data/ccle_mutations.csv")

# === Upload All Files ===
blob_service = BlobServiceClient.from_connection_string(conn_str)
container_client = blob_service.get_container_client(container_name)

# Create container if needed
try:
    container_client.create_container()
except Exception:
    pass  # Ignore if it already exists

# Upload loop
for filename in files_to_upload:
    file_path = os.path.join(local_raw_folder, filename)
    if os.path.exists(file_path):
        print(f"Uploading {filename}...")
        with open(file_path, "rb") as data:
            container_client.upload_blob(name=filename, data=data, overwrite=True)
    else:
        print(f"File not found: {filename}")
