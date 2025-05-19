import os
import pandas as pd
import re

# === Paths ===
input_folder = "/opt/airflow/data/ingested_data/"
output_folder = "/opt/airflow/data/processed_data/"
os.makedirs(output_folder, exist_ok=True)

# === Column cleaner ===
def clean_columns(df):
    df.columns = [
        re.sub(r'_+', '_', re.sub(r'\W+', '_', col.strip().lower())).strip('_')
        for col in df.columns
    ]
    return df

# === Datasets to load ===
datasets = {
    "brca": "brca_data_w_subtypes.csv",
    "glioblastoma": "glioblastoma_multiforme_dead___sheet1.csv",
    "depmap": "ccle_mutations.csv",
    "data": "data.csv"
}

# === Process & save ===
log_path = os.path.join(output_folder, "processing_log.txt")
with open(log_path, "w") as log_file:
    for name, filename in datasets.items():
        file_path = os.path.join(input_folder, filename)
        try:
            df = pd.read_csv(file_path, low_memory=False)

            # Special filtering for depmap
            if name == "depmap":
                keep_cols = [
                    "Hugo_Symbol", "Variant_Classification", "Variant_Type",
                    "Tumor_Seq_Allele1", "Genome_Change", "DepMap_ID", 
                    "isDeleterious", "isTCGAhotspot", "ExAC_AF"
                ]
                df = df[keep_cols]

            df = clean_columns(df)
            missing = df.isnull().sum().sum()
            shape = df.shape

            output_file = os.path.join(output_folder, f"{name}_clean.csv")
            df.to_csv(output_file, index=False)

            print(f"Processed {name}: shape={shape}, missing={missing}")
            log_file.write(f"{name}: shape={shape}, missing={missing}\n")

        except Exception as e:
            print(f"Failed to process {name}: {e}")
            log_file.write(f"{name}: FAILED - {e}\n")
