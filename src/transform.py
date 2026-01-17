import pandas as pd
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
RAW_DATA_PATH = SCRIPT_DIR.parent / "data" / "raw" / "bank.csv"
PROCESSED_DATA_PATH = SCRIPT_DIR.parent / "data" / "processed" / "bank_cleaned.csv"

def transform_data(input_path=None, output_path=None):
    """Load raw CSV, clean/transform it, save processed CSV."""
    
    input_path = Path(input_path) if input_path else RAW_DATA_PATH
    output_path = Path(output_path) if output_path else PROCESSED_DATA_PATH

    df = pd.read_csv(input_path)

    df.columns = df.columns.str.strip().str.lower()

    if "default" in df.columns:
        df.rename(columns={"default": "default_flag"}, inplace=True)

    for col in ["housing", "loan", "default_flag", "deposit"]:
        if col in df.columns:
            df[col] = df[col].replace({"yes": 1, "no": 0})
        else:
            df[col] = 0

    if "contact_date" in df.columns:
        df["contact_date"] = pd.to_datetime(df["contact_date"], errors="coerce")
    else:
        df["contact_date"] = pd.Timestamp.today()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Transformed data saved at: {output_path}")

    return df

if __name__ == "__main__":
    transform_data()
