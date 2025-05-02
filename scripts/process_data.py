import pandas as pd
import os

input_dir = "data/ingested_data/"
output_dir = "data/processed_data/"
os.makedirs(output_dir, exist_ok=True)

# Load & process each dataset
brca = pd.read_csv(os.path.join(input_dir, "brca_data_w_subtypes.csv"))
glioblastoma = pd.read_csv(os.path.join(input_dir, "Glioblastoma Multiforme Dead - Sheet1.csv"))
depmap = pd.read_csv(os.path.join(input_dir, "CCLE_mutations.csv"))
data = pd.read_csv(os.path.join(input_dir, "data.csv"))

# Optionally: filter / clean / validate
print(f"BRCA shape: {brca.shape}")
print(f"Glioblastoma shape: {glioblastoma.shape}")
print(f"DepMap shape: {depmap.shape}")
print(f"TCGA 'data' shape: {data.shape}")

# Save for now (unmodified, just processed copies)
brca.to_csv(os.path.join(output_dir, "brca_clean.csv"), index=False)
glioblastoma.to_csv(os.path.join(output_dir, "glioblastoma_clean.csv"), index=False)
depmap.to_csv(os.path.join(output_dir, "depmap_clean.csv"), index=False)
data.to_csv(os.path.join(output_dir, "data_clean.csv"), index=False)
