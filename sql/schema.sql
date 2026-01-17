CREATE TABLE IF NOT EXISTS customers (
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


CREATE TABLE IF NOT EXISTS campaigns (
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


CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    deposit INTEGER,
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
);
