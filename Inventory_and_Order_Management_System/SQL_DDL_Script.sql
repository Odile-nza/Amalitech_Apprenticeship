-- STEP 1 — DROP TABLES IF THEY EXIST

DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS inventory CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS customers CASCADE;

-- TABLE 1 - CUSTOMERS
-- Stores information about customers who place orders
-- One customer can have many orders (One-to-Many)

CREATE TABLE customers (
   customer_id      SERIAL             PRIMARY KEY,
   full_name        VARCHAR(100)       NOT NULL,
   email            VARCHAR(100)       NOT NULL UNIQUE,
   phone            VARCHAR(20),
   shipping_address TEXT
);

-- TABLE 2 - Products
-- Stores information about products available for sale
-- One product can appear in many orders (Many-to-Many)

CREATE TABLE products (
product_id   SERIAL        PRIMARY KEY,
product_name VARCHAR(100)  NOT NULL,
category     VARCHAR(50),
price        DECIMAL(10,2) NOT NULL,

-- Price must always be non-negative
CONSTRAINT chk_product_price CHECK (price >= 0)
);

-- TABLE 3 - INVENTORY
-- Tracks current stock level for each product
-- One product has one inventory record (One-to-One)

CREATE TABLE inventory (
    inventory_id  SERIAL   PRIMARY KEY,
	product_id    INT      NOT NULL UNIQUE,
	quantity      INT      NOT NULL DEFAULT 0,

	-- Stock level must always be non-negative
	CONSTRAINT chk_inventory_quantity CHECK (quantity >=0),

	-- Link to products table
	CONSTRAINT fk_inventory_product
	    FOREIGN KEY (product_id)
		REFERENCES products (product_id)
		ON DELETE CASCADE
);

-- TABLE 4 — ORDERS
-- Stores order header information
-- One customer can have many orders (One-to-Many)
-- One order can have many items (One-to-Many)

CREATE TABLE orders (
    order_id     SERIAL          PRIMARY KEY,
    customer_id  INT             NOT NULL,
    order_date   DATE            NOT NULL DEFAULT CURRENT_DATE,
    total_amount DECIMAL(10, 2)  DEFAULT 0.00,
    order_status VARCHAR(20)     NOT NULL DEFAULT 'Pending',

    -- Status must be one of these three values
    CONSTRAINT chk_order_status
        CHECK (order_status IN ('Pending', 'Shipped', 'Delivered')),

    -- Total amount must be non-negative
    CONSTRAINT chk_total_amount
        CHECK (total_amount >= 0),

    -- Link to customers table
    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers (customer_id)
        ON DELETE CASCADE
);

-- TABLE 5 — ORDER ITEMS
-- Bridge table that links orders and products
-- Solves the Many-to-Many relationship between orders and products
-- One order can contain many products
-- One product can appear in many orders

CREATE TABLE order_items (
    order_item_id     SERIAL         PRIMARY KEY,
    order_id          INT            NOT NULL,
    product_id        INT            NOT NULL,
    quantity          INT            NOT NULL,
    price_at_purchase DECIMAL(10, 2) NOT NULL,

    -- Quantity must be at least 1
    CONSTRAINT chk_order_item_quantity
        CHECK (quantity > 0),

    -- Price at purchase must be non-negative
    CONSTRAINT chk_price_at_purchase
        CHECK (price_at_purchase >= 0),

    -- Link to orders table
    CONSTRAINT fk_order_items_order
        FOREIGN KEY (order_id)
        REFERENCES orders (order_id)
        ON DELETE CASCADE,

    -- Link to products table
    CONSTRAINT fk_order_items_product
        FOREIGN KEY (product_id)
        REFERENCES products (product_id)
        ON DELETE CASCADE
);

-- VERIFY — CHECK ALL TABLES WERE CREATED
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;