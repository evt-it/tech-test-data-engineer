-- Seed exactly 100 historical orders.
--
-- Timestamps are generated relative to now() so they are always 7-30 days in
-- the past regardless of when the stack is first started. This guarantees the
-- seed data alone can never satisfy a recent-data freshness check.
--
-- NOTE: the catalogue below mirrors event-source/catalogue.py. If you change
-- products there, update this file to match.

WITH catalogue (product_id, product_name, category, unit_price) AS (
    VALUES
        ('SKU-001', 'Wireless Headphones',    'Electronics',       79.99::numeric(10,2)),
        ('SKU-002', 'Bluetooth Speaker',      'Electronics',       49.50),
        ('SKU-003', 'USB-C Charging Cable',   'Electronics',       12.95),
        ('SKU-004', 'Espresso Machine',       'Home & Kitchen',   249.00),
        ('SKU-005', 'Chef''s Knife 20cm',     'Home & Kitchen',    89.95),
        ('SKU-006', 'Cast Iron Skillet',      'Home & Kitchen',    64.50),
        ('SKU-007', 'Yoga Mat',               'Sports & Outdoors', 34.99),
        ('SKU-008', 'Insulated Water Bottle', 'Sports & Outdoors', 27.50),
        ('SKU-009', 'Trail Running Shoes',    'Sports & Outdoors',139.95),
        ('SKU-010', 'Hardcover Notebook A5',  'Stationery',        18.75),
        ('SKU-011', 'Fountain Pen',           'Stationery',        42.00),
        ('SKU-012', 'Scented Soy Candle',     'Home Fragrance',    24.95)
),
picks AS (
    SELECT
        gen_random_uuid() AS order_id,
        gen_random_uuid() AS customer_id,
        (1 + floor(random() * 12))::int AS catalogue_row,
        (1 + floor(random() * 5))::int  AS quantity,
        now() - (interval '7 days' + random() * interval '23 days') AS order_ts
    FROM generate_series(1, 100)
)
INSERT INTO sales.orders
    (order_id, customer_id, product_id, product_name, category,
     quantity, unit_price, total_amount, order_ts)
SELECT
    p.order_id,
    p.customer_id,
    c.product_id,
    c.product_name,
    c.category,
    p.quantity,
    c.unit_price,
    (p.quantity * c.unit_price)::numeric(10,2),
    p.order_ts
FROM picks p
JOIN (SELECT row_number() OVER () AS rn, * FROM catalogue) c
  ON c.rn = p.catalogue_row;
