"""Product catalogue for the event source.

NOTE: postgres/init/02-seed.sql contains the same catalogue as a SQL VALUES
list. If you change products here, update the seed file to match.
"""

PRODUCTS = [
    {"product_id": "SKU-001", "product_name": "Wireless Headphones", "category": "Electronics", "unit_price": 79.99},
    {"product_id": "SKU-002", "product_name": "Bluetooth Speaker", "category": "Electronics", "unit_price": 49.50},
    {"product_id": "SKU-003", "product_name": "USB-C Charging Cable", "category": "Electronics", "unit_price": 12.95},
    {"product_id": "SKU-004", "product_name": "Espresso Machine", "category": "Home & Kitchen", "unit_price": 249.00},
    {"product_id": "SKU-005", "product_name": "Chef's Knife 20cm", "category": "Home & Kitchen", "unit_price": 89.95},
    {"product_id": "SKU-006", "product_name": "Cast Iron Skillet", "category": "Home & Kitchen", "unit_price": 64.50},
    {"product_id": "SKU-007", "product_name": "Yoga Mat", "category": "Sports & Outdoors", "unit_price": 34.99},
    {"product_id": "SKU-008", "product_name": "Insulated Water Bottle", "category": "Sports & Outdoors", "unit_price": 27.50},
    {"product_id": "SKU-009", "product_name": "Trail Running Shoes", "category": "Sports & Outdoors", "unit_price": 139.95},
    {"product_id": "SKU-010", "product_name": "Hardcover Notebook A5", "category": "Stationery", "unit_price": 18.75},
    {"product_id": "SKU-011", "product_name": "Fountain Pen", "category": "Stationery", "unit_price": 42.00},
    {"product_id": "SKU-012", "product_name": "Scented Soy Candle", "category": "Home Fragrance", "unit_price": 24.95},
]
