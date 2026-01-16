import pandas as pd
import sqlite3
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
CSV_PATH = SCRIPT_DIR.parent / "data" / "processed" / "bank_cleaned.csv"
DB_PATH = SCRIPT_DIR.parent / "data" / "bankview.db"

def run_etl():
    # Load processed CSV
    df = pd.read_csv(CSV_PATH)

    # Rename 'default' column to avoid SQL reserved keyword
    df.rename(columns={"default": "default_flag"}, inplace=True)

    # Connect to SQLite database (creates it if not exists)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create tables
    cursor.executescript("""
    DROP TABLE IF EXISTS products;
    DROP TABLE IF EXISTS campaigns;
    DROP TABLE IF EXISTS customers;

    CREATE TABLE customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        age INTEGER,
        job TEXT,
        marital TEXT,
        education TEXT,
        default_flag INTEGER,
        balance INTEGER,
        housing INTEGER,
        loan INTEGER
    );

    CREATE TABLE campaigns (
        campaign_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        contact_date DATE,
        contact TEXT,
        duration INTEGER,
        campaign_number INTEGER,
        pdays INTEGER,
        previous INTEGER,
        poutcome TEXT,
        FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
    );

    CREATE TABLE products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        deposit INTEGER,
        FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
    );
    """)

    # Insert data
    for idx, row in df.iterrows():
        # Insert into customers
        cursor.execute("""
            INSERT INTO customers (age, job, marital, education, default_flag, balance, housing, loan)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (row.age, row.job, row.marital, row.education, row.default_flag,
              row.balance, row.housing, row.loan))
        
        customer_id = cursor.lastrowid

        # Insert into campaigns
        cursor.execute("""
            INSERT INTO campaigns (customer_id, contact_date, contact, duration,
                                   campaign_number, pdays, previous, poutcome)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (customer_id, row.contact_date, row.contact, row.duration,
              row.campaign, row.pdays, row.previous, row.poutcome))

        # Insert into products
        cursor.execute("""
            INSERT INTO products (customer_id, deposit)
            VALUES (?, ?)
        """, (customer_id, row.deposit))

    # Commit and close
    conn.commit()
    conn.close()

    print(f"ETL completed! Database saved at {DB_PATH}")

if __name__ == "__main__":
    run_etl()
