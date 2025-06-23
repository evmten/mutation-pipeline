import os
import pandas as pd
import re

# Input and output folders
input_folder = "/opt/airflow/data/ingested_data/"
output_folder = "/opt/airflow/data/transformed_data/"
os.makedirs(output_folder, exist_ok=True)

# Function to clean column names
def clean_columns(df):
    df.columns = [
        re.sub(r'_+', '_', re.sub(r'\W+', '_', col.strip().lower())).strip('_')
        for col in df.columns
    ]
    return df

# Datasets to process
datasets = {
    "brca": "brca_data_w_subtypes.csv",
    "glioblastoma": "glioblastoma_multiforme_dead___sheet1.csv",
    "depmap": "ccle_mutations.csv",
    "data": "data.csv"
}

# Log file path
log_path = os.path.join(output_folder, "transforming_log.txt")
with open(log_path, "w") as log_file:
    for name, filename in datasets.items():
        file_path = os.path.join(input_folder, filename)
        try:
            df = pd.read_csv(file_path, low_memory=False)

            # Specific columns to keep for 'depmap'
            if name == "depmap":
                keep_cols = [
                    "Hugo_Symbol", "Variant_Classification", "Variant_Type",
                    "Tumor_Seq_Allele1", "Genome_Change", "DepMap_ID", 
                    "isDeleterious", "isTCGAhotspot", "ExAC_AF"
                ]
                df = df[keep_cols]

            # Clean column names
            df = clean_columns(df)

            # Calculate missing values and shape
            missing = df.isnull().sum().sum()
            shape = df.shape

            # Output transformed file
            output_file = os.path.join(output_folder, f"{name}_clean.csv")
            df.to_csv(output_file, index=False)

            # Log transformation details
            print(f"Transformed {name}: shape={shape}, missing={missing}")
            log_file.write(f"{name}: shape={shape}, missing={missing}\n")

        except Exception as e:
            # Log any errors encountered
            print(f"Failed to transform {name}: {e}")
            log_file.write(f"{name}: FAILED - {e}\n")
