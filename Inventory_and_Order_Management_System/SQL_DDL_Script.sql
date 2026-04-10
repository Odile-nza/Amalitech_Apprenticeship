-- ============================================================
--  DDL SCRIPT: Inventory and Order Management System
-- ============================================================


-- STEP 1 — DROP EXISTING TABLES
-- ============================================================
-- Drop in reverse dependency order to avoid FK conflicts
-- CASCADE drops dependent objects automatically

DROP TABLE IF EXISTS order_audit     CASCADE;
DROP TABLE IF EXISTS inventory_log   CASCADE;
DROP TABLE IF EXISTS order_items     CASCADE;
DROP TABLE IF EXISTS orders          CASCADE;
DROP TABLE IF EXISTS inventory       CASCADE;
DROP TABLE IF EXISTS products        CASCADE;
DROP TABLE IF EXISTS customers       CASCADE;


-- TABLE 1 — CUSTOMERS
-- ============================================================
-- Stores customer information including tier classification
-- Customer tier is automatically assigned based on spending:
-- Bronze < $500 | Silver $500-$2000 | Gold > $2000

CREATE TABLE customers (
    customer_id      SERIAL          PRIMARY KEY,
    full_name        VARCHAR(100)    NOT NULL,
    email            VARCHAR(100)    NOT NULL UNIQUE,
    phone            VARCHAR(20),
    shipping_address TEXT,

    -- Customer tier for loyalty program and bulk discounts
    -- Why VARCHAR with CHECK: enforces valid tier values
    -- without needing a separate lookup table
    customer_tier    VARCHAR(10)     NOT NULL DEFAULT 'Bronze',

    CONSTRAINT chk_customer_tier
        CHECK (customer_tier IN ('Bronze', 'Silver', 'Gold'))
);


-- TABLE 2 — PRODUCTS
-- ============================================================
-- Stores product details with pricing information

CREATE TABLE products (
    product_id   SERIAL         PRIMARY KEY,
    product_name VARCHAR(100)   NOT NULL,
    category     VARCHAR(50),
    price        DECIMAL(10, 2) NOT NULL,

    -- Price must always be non-negative
    CONSTRAINT chk_product_price CHECK (price >= 0)
);


-- TABLE 3 — INVENTORY
-- ============================================================
-- Tracks current stock level and reorder threshold
-- per product

CREATE TABLE inventory (
    inventory_id  SERIAL  PRIMARY KEY,
    product_id    INT     NOT NULL UNIQUE,
    quantity      INT     NOT NULL DEFAULT 0,

    -- Reorder level: minimum stock before restocking needed
    -- Why: Enables automated low-stock alerts and reorder views
    -- When quantity drops below reorder_level → alert triggered
    reorder_level INT     NOT NULL DEFAULT 10,

    -- Last time inventory was updated — for audit trail
    last_updated  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_inventory_quantity
        CHECK (quantity >= 0),

    CONSTRAINT chk_reorder_level
        CHECK (reorder_level >= 0),

    CONSTRAINT fk_inventory_product
        FOREIGN KEY (product_id)
        REFERENCES products (product_id)
        ON DELETE CASCADE
);


-- TABLE 4 — ORDERS
-- ============================================================
-- Stores order header information per customer

CREATE TABLE orders (
    order_id     SERIAL          PRIMARY KEY,
    customer_id  INT             NOT NULL,

    order_date   TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,

    total_amount DECIMAL(10, 2)  DEFAULT 0.00,
    order_status VARCHAR(20)     NOT NULL DEFAULT 'Pending',

    CONSTRAINT chk_order_status
        CHECK (order_status IN ('Pending', 'Shipped', 'Delivered', 'Cancelled')),

    CONSTRAINT chk_total_amount
        CHECK (total_amount >= 0),

    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers (customer_id)
        ON DELETE CASCADE
);


-- TABLE 5 — ORDER ITEMS
-- ============================================================
-- Bridge table linking orders to multiple products
-- One order can contain many products (Many-to-Many)

CREATE TABLE order_items (
    order_item_id     SERIAL         PRIMARY KEY,
    order_id          INT            NOT NULL,
    product_id        INT            NOT NULL,
    quantity          INT            NOT NULL,
    price_at_purchase DECIMAL(10, 2) NOT NULL,

    -- Discount applied at time of purchase
    -- Why: Captures bulk discounts and promotions
    -- at the exact moment of purchase for accurate reporting
    discount_percent  DECIMAL(5, 2)  NOT NULL DEFAULT 0.00,

    -- Final price after discount applied
    final_price       DECIMAL(10, 2) NOT NULL,

    CONSTRAINT chk_order_item_quantity
        CHECK (quantity > 0),

    CONSTRAINT chk_price_at_purchase
        CHECK (price_at_purchase >= 0),

    CONSTRAINT chk_discount_percent
        CHECK (discount_percent BETWEEN 0 AND 100),

    CONSTRAINT fk_order_items_order
        FOREIGN KEY (order_id)
        REFERENCES orders (order_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_order_items_product
        FOREIGN KEY (product_id)
        REFERENCES products (product_id)
        ON DELETE CASCADE
);


-- TABLE 6 — INVENTORY LOG (AUDIT TABLE)
-- ============================================================
-- Records every change made to inventory stock levels
-- Why: Provides a complete audit trail for stock changes
-- Answers: when did stock change? why? what was previous value?

CREATE TABLE inventory_log (
    log_id          SERIAL          PRIMARY KEY,
    product_id      INT             NOT NULL,

    -- Stock level before and after the change
    previous_quantity INT           NOT NULL,
    new_quantity      INT           NOT NULL,

    -- How much stock changed (positive = added, negative = removed)
    quantity_change   INT           NOT NULL,

    -- Reason for the stock change
    -- Why: Essential for auditing and inventory management
    change_reason   VARCHAR(50)     NOT NULL,

    CONSTRAINT chk_change_reason
        CHECK (change_reason IN (
            'ORDER_PLACED',      -- stock reduced by customer order
            'ORDER_CANCELLED',   -- stock restored on cancellation
            'RESTOCK',           -- new stock added manually
            'ADJUSTMENT',        -- manual correction
            'DAMAGED'            -- stock removed due to damage
        )),

    order_id        INT,
    changed_at      TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    changed_by      VARCHAR(100)    DEFAULT 'SYSTEM',

    CONSTRAINT fk_inventory_log_product
        FOREIGN KEY (product_id)
        REFERENCES products (product_id),

    CONSTRAINT fk_inventory_log_order
        FOREIGN KEY (order_id)
        REFERENCES orders (order_id)
);


-- TABLE 7 — ORDER AUDIT TABLE
-- ============================================================
-- Tracks the complete lifecycle of each order
-- Why: Records every status change for compliance and support
-- Answers: when was order placed? shipped? delivered?

CREATE TABLE order_audit (
    audit_id        SERIAL          PRIMARY KEY,
    order_id        INT             NOT NULL,
    customer_id     INT             NOT NULL,

    
    previous_status VARCHAR(20),
    new_status      VARCHAR(20)     NOT NULL,

    changed_at      TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,

    changed_by      VARCHAR(100)    DEFAULT 'SYSTEM',

    notes           TEXT,

    CONSTRAINT fk_order_audit_order
        FOREIGN KEY (order_id)
        REFERENCES orders (order_id),

    CONSTRAINT fk_order_audit_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers (customer_id)
);


-- PERFORMANCE OPTIMIZATION — INDEXES
-- ============================================================
-- Indexes speed up queries on frequently searched columns
-- Why: Without indexes PostgreSQL scans every row (slow)
-- With indexes it jumps directly to matching rows (fast)
-- Trade-off: indexes use extra storage and slow down writes
-- but dramatically speed up reads on large datasets

-- Index on orders.customer_id
-- Why: Most order queries filter or join by customer_id
-- e.g. "find all orders for customer X"
CREATE INDEX idx_orders_customer_id
    ON orders (customer_id);

-- Index on order_items.order_id
-- Why: order_items is frequently joined with orders
-- e.g. "find all items in order X"
CREATE INDEX idx_order_items_order_id
    ON order_items (order_id);

-- Index on order_items.product_id
-- Why: Frequently joined with products table
-- e.g. "find all orders containing product X"
CREATE INDEX idx_order_items_product_id
    ON order_items (product_id);

-- Index on inventory.product_id
-- Why: Stock checks always filter by product_id
CREATE INDEX idx_inventory_product_id
    ON inventory (product_id);

-- Index on inventory_log.product_id
-- Why: Audit queries filter by product_id
CREATE INDEX idx_inventory_log_product_id
    ON inventory_log (product_id);

-- Index on orders.order_date
-- Why: Time-based queries and trend analysis filter by date
CREATE INDEX idx_orders_order_date
    ON orders (order_date);

-- Index on customers.customer_tier
-- Why: Customer tier queries for discount calculations
CREATE INDEX idx_customers_tier
    ON customers (customer_tier);


-- VIEWS
-- ============================================================

-- VIEW 1 — CustomerSalesSummary
-- Pre-calculates customer spending and tier information
DROP VIEW IF EXISTS CustomerSalesSummary;

CREATE VIEW CustomerSalesSummary AS
SELECT
    c.customer_id,
    c.full_name,
    c.email,
    c.customer_tier,
    COUNT(DISTINCT o.order_id)              AS total_orders,
    SUM(oi.quantity)                        AS total_items_purchased,
    SUM(oi.final_price)                     AS total_amount_spent,
    ROUND(AVG(oi.final_price), 2)           AS avg_order_value,
    MIN(o.order_date)                       AS first_order_date,
    MAX(o.order_date)                       AS last_order_date
FROM customers c
JOIN orders o       ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id    = oi.order_id
GROUP BY c.customer_id, c.full_name, c.email, c.customer_tier;


-- VIEW 2 — LowStockAlert
-- Shows products that have fallen below their reorder level
-- Why: Enables automated restocking alerts and prevents
-- stockouts that would cause failed customer orders

DROP VIEW IF EXISTS LowStockAlert;

CREATE VIEW LowStockAlert AS
SELECT
    p.product_id,
    p.product_name,
    p.category,
    p.price,
    i.quantity          AS current_stock,
    i.reorder_level,
    i.quantity - i.reorder_level AS stock_gap,

    -- Stock status classification
    CASE
        WHEN i.quantity = 0              THEN 'OUT OF STOCK'
        WHEN i.quantity < i.reorder_level THEN 'LOW STOCK'
        ELSE                                  'SUFFICIENT'
    END AS stock_status,

    i.last_updated
FROM products p
JOIN inventory i ON p.product_id = i.product_id
ORDER BY i.quantity ASC;


-- VIEW 3 — InventoryAuditHistory
-- Shows complete history of all inventory changes
-- Why: Essential for auditing and compliance reporting

DROP VIEW IF EXISTS InventoryAuditHistory;

CREATE VIEW InventoryAuditHistory AS
SELECT
    il.log_id,
    p.product_name,
    p.category,
    il.previous_quantity,
    il.new_quantity,
    il.quantity_change,
    il.change_reason,
    il.order_id,
    il.changed_at,
    il.changed_by
FROM inventory_log il
JOIN products p ON il.product_id = p.product_id
ORDER BY il.changed_at DESC;


-- VERIFY ALL TABLES AND INDEXES CREATED
-- ============================================================

-- Check tables
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;

-- Check indexes
SELECT indexname, tablename
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY tablename;