import pandas as pd
import os
import re

input_dir = "/opt/airflow/data/ingested_data/"
output_dir = "/opt/airflow/data/processed_data/"
os.makedirs(output_dir, exist_ok=True)

def clean_columns(df):
    df.columns = [
        re.sub(r'_+', '_', re.sub(r'\W+', '_', col.strip().lower())).strip('_')
        # re.sub(r'\W+', '_', col.strip().lower())
        for col in df.columns
    ]
    return df

# def report_missing(df, name):
#     total_missing = df.isnull().sum().sum()
#     print(f"→ {name}: Missing values = {total_missing}")
#     return total_missing

# Load and clean each dataset
datasets = {
    "brca": pd.read_csv(os.path.join(input_dir, "brca_data_w_subtypes.csv")),
    "glioblastoma": pd.read_csv(os.path.join(input_dir, "glioblastoma_multiforme_dead___sheet1.csv")),
    "depmap": pd.read_csv(os.path.join(input_dir, "ccle_mutations.csv"), low_memory=False),
    # "depmap": pd.read_csv(os.path.join(input_dir, "CCLE_mutations.csv"))
    "data": pd.read_csv(os.path.join(input_dir, "data.csv")),
}

# Process and save
log_path = os.path.join(output_dir, "processing_log.txt")
with open(log_path, "w") as log_file:
    for name, df in datasets.items():

        if name == "depmap":
            print(df.columns)
            keep_cols = [
                "Hugo_Symbol", "Variant_Classification", "Variant_Type",
                "Tumor_Seq_Allele1", "Genome_Change", "DepMap_ID", 
                "isDeleterious", "isTCGAhotspot", "ExAC_AF"
            ]
            df = df[keep_cols]
            print(df.columns)

        df = clean_columns(df)
        missing = df.isnull().sum().sum()
        print(f"→ {name}: shape={df.shape}, missing={missing}")
        log_file.write(f"{name}: shape={df.shape}, missing={missing}\n")
        df.to_csv(os.path.join(output_dir, f"{name}_clean.csv"), index=False)
        