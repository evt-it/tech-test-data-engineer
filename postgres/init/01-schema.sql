-- Database "sales" is created by the postgres image (POSTGRES_DB).
-- This script runs inside it.

CREATE SCHEMA IF NOT EXISTS sales;

CREATE TABLE sales.orders (
    order_id     UUID PRIMARY KEY,
    customer_id  UUID NOT NULL,
    product_id   VARCHAR NOT NULL,
    product_name VARCHAR NOT NULL,
    category     VARCHAR NOT NULL,
    quantity     INTEGER NOT NULL,
    unit_price   NUMERIC(10, 2) NOT NULL,
    total_amount NUMERIC(10, 2) NOT NULL,
    order_ts     TIMESTAMPTZ NOT NULL
);
