SELECT
    COUNT(*) AS total_customers,
    SUM(deposit) AS subscribed_customers,
    ROUND(100.0 * SUM(deposit) / COUNT(*), 2) AS conversion_rate_percent
FROM products;


SELECT
    c.contact,
    COUNT(*) AS total_contacts,
    SUM(p.deposit) AS successful_conversions,
    ROUND(100.0 * SUM(p.deposit) / COUNT(*), 2) AS conversion_rate_percent
FROM campaigns c
JOIN products p ON c.customer_id = p.customer_id
GROUP BY c.contact
ORDER BY conversion_rate_percent DESC;


SELECT
    p.deposit AS subscribed,
    ROUND(AVG(c.balance), 2) AS avg_balance
FROM customers c
JOIN products p ON c.customer_id = p.customer_id
GROUP BY p.deposit;


SELECT
    c.job,
    COUNT(*) AS total_customers,
    SUM(p.deposit) AS conversions,
    ROUND(100.0 * SUM(p.deposit) / COUNT(*), 2) AS conversion_rate_percent
FROM customers c
JOIN products p ON c.customer_id = p.customer_id
GROUP BY c.job
ORDER BY conversion_rate_percent DESC;


SELECT
    campaign_number,
    COUNT(*) AS total_customers,
    SUM(p.deposit) AS conversions,
    ROUND(100.0 * SUM(p.deposit) / COUNT(*), 2) AS conversion_rate_percent
FROM campaigns c
JOIN products p ON c.customer_id = p.customer_id
GROUP BY campaign_number
ORDER BY campaign_number;


SELECT
    CASE
        WHEN age < 30 THEN 'Under 30'
        WHEN age BETWEEN 30 AND 45 THEN '30–45'
        WHEN age BETWEEN 46 AND 60 THEN '46–60'
        ELSE '60+'
    END AS age_group,
    COUNT(*) AS total_customers,
    SUM(p.deposit) AS conversions,
    ROUND(100.0 * SUM(p.deposit) / COUNT(*), 2) AS conversion_rate_percent
FROM customers c
JOIN products p ON c.customer_id = p.customer_id
GROUP BY age_group
ORDER BY age_group;


SELECT
    c.loan,
    COUNT(*) AS total_customers,
    SUM(p.deposit) AS conversions,
    ROUND(100.0 * SUM(p.deposit) / COUNT(*), 2) AS conversion_rate_percent
FROM customers c
JOIN products p ON c.customer_id = p.customer_id
GROUP BY c.loan;


SELECT
    contact_date,
    COUNT(*) AS total_contacts,
    SUM(p.deposit) AS conversions,
    ROUND(100.0 * SUM(p.deposit) / COUNT(*), 2) AS conversion_rate_percent
FROM campaigns c
JOIN products p ON c.customer_id = p.customer_id
GROUP BY contact_date
ORDER BY contact_date;


SELECT
    c.customer_id,
    c.job,
    c.balance,
    c.education,
    c.marital
FROM customers c
JOIN products p ON c.customer_id = p.customer_id
WHERE p.deposit = 1
ORDER BY c.balance DESC
LIMIT 10;
