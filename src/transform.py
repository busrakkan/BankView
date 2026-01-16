from pathlib import Path
import pandas as pd

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent

# Build paths relative to the script
RAW_DATA_PATH = SCRIPT_DIR.parent / "data" / "raw" / "bank.csv"
PROCESSED_DATA_PATH = SCRIPT_DIR.parent / "data" / "processed" / "bank_cleaned.csv"


def transform_data():
    # Load raw data
    df = pd.read_csv(RAW_DATA_PATH)

    # Standardize column names
    df.columns = df.columns.str.lower().str.strip()

    # Normalize yes/no categorical fields
    yes_no_cols = ["default", "housing", "loan", "deposit"]
    for col in yes_no_cols:
        df[col] = df[col].map({"yes": 1, "no": 0})

    # Combine day and month into a single date column
    df["contact_date"] = pd.to_datetime(
        df["day"].astype(str) + "-" + df["month"] + "-2023",
        format="%d-%b-%Y",
        errors="coerce"
    )

    # Drop original day and month columns
    df.drop(columns=["day", "month"], inplace=True)

    # Handle missing or invalid values (if any)
    df.fillna(0, inplace=True)

    # Save processed data
    PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_DATA_PATH, index=False)

    print("Data transformation completed successfully.")

if __name__ == "__main__":
    transform_data()
