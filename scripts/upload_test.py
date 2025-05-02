from azure.storage.blob import BlobServiceClient
import os
from dotenv import load_dotenv

load_dotenv()

conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
container = os.getenv("CONTAINER_NAME")

blob_service = BlobServiceClient.from_connection_string(conn_str)
container_client = blob_service.get_container_client(container)

# Test upload
with open("data/test.json", "w") as f:
    f.write('{"sample_id": "TCGA-01", "gene": "TP53", "mutation": 1}')

with open("data/test.json", "rb") as data:
    container_client.upload_blob("test.json", data, overwrite=True)

print("Uploaded test file to Azure Blob.")
