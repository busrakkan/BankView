from pathlib import Path
import pandas as pd

SCRIPT_DIR = Path(__file__).parent

RAW_DATA_PATH = SCRIPT_DIR.parent / "data" / "raw" / "bank.csv"
PROCESSED_DATA_PATH = SCRIPT_DIR.parent / "data" / "processed" / "bank_cleaned.csv"


def transform_data():
    df = pd.read_csv(RAW_DATA_PATH)

    df.columns = df.columns.str.lower().str.strip()

    yes_no_cols = ["default", "housing", "loan", "deposit"]
    for col in yes_no_cols:
        df[col] = df[col].map({"yes": 1, "no": 0})

    df["contact_date"] = pd.to_datetime(
        df["day"].astype(str) + "-" + df["month"] + "-2023",
        format="%d-%b-%Y",
        errors="coerce"
    )

    df.drop(columns=["day", "month"], inplace=True)

    df.fillna(0, inplace=True)

    PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_DATA_PATH, index=False)

    print("Data transformation completed successfully.")

if __name__ == "__main__":
    transform_data()
