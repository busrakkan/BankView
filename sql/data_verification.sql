SELECT 'customers' AS table_name, COUNT(*) AS row_count FROM customers;
SELECT 'campaigns' AS table_name, COUNT(*) AS row_count FROM campaigns;
SELECT 'products' AS table_name, COUNT(*) AS row_count FROM products;


SELECT COUNT(*) AS null_critical_fields
FROM customers
WHERE age IS NULL
   OR job IS NULL
   OR marital IS NULL
   OR education IS NULL
   OR balance IS NULL;


SELECT COUNT(*) AS orphan_campaign_records
FROM campaigns c
LEFT JOIN customers cu
ON c.customer_id = cu.customer_id
WHERE cu.customer_id IS NULL;


SELECT DISTINCT deposit FROM products;
SELECT DISTINCT default_flag FROM customers;
SELECT DISTINCT housing FROM customers;
SELECT DISTINCT loan FROM customers;

SELECT
    deposit,
    COUNT(*) AS customers
FROM products
GROUP BY deposit;

SELECT
    p.deposit,
    ROUND(AVG(c.balance), 2) AS avg_balance
FROM customers c
JOIN products p
ON c.customer_id = p.customer_id
GROUP BY p.deposit;

SELECT
    c.customer_id,
    c.age,
    c.job,
    c.balance,
    p.deposit,
    ca.contact_date,
    ca.duration
FROM customers c
JOIN products p ON c.customer_id = p.customer_id
JOIN campaigns ca ON c.customer_id = ca.customer_id
LIMIT 10;
