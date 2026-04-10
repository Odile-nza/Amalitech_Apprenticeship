-- DML SCRIPT  Inventory and Order Management System
-- ============================================================

-- SECTION 1: SAMPLE DATA
-- ============================================================

-- CUSTOMERS (10 customers with tiers)
INSERT INTO customers (full_name, email, phone, shipping_address, customer_tier) VALUES
('Alice Johnson',   'alice.johnson@email.com',   '+1-555-0101', '123 Main St, New York',       'Gold'),
('Bob Smith',       'bob.smith@email.com',        '+1-555-0102', '456 Oak Ave, Los Angeles',    'Silver'),
('Carol Williams',  'carol.williams@email.com',   '+1-555-0103', '789 Pine Rd, Chicago',        'Bronze'),
('David Brown',     'david.brown@email.com',      '+1-555-0104', '321 Elm St, Houston',         'Gold'),
('Emma Davis',      'emma.davis@email.com',        '+1-555-0105', '654 Maple Dr, Phoenix',       'Silver'),
('Frank Miller',    'frank.miller@email.com',     '+1-555-0106', '987 Cedar Ln, Philadelphia',  'Bronze'),
('Grace Wilson',    'grace.wilson@email.com',     '+1-555-0107', '147 Birch Blvd, San Antonio', 'Silver'),
('Henry Moore',     'henry.moore@email.com',      '+1-555-0108', '258 Walnut St, San Diego',    'Bronze'),
('Isabel Taylor',   'isabel.taylor@email.com',    '+1-555-0109', '369 Spruce Ave, Dallas',      'Gold'),
('James Anderson',  'james.anderson@email.com',   '+1-555-0110', '741 Ash Ct, San Jose',        'Bronze');

-- PRODUCTS (10 products across 3 categories)
INSERT INTO products (product_name, category, price) VALUES
('Laptop Pro 15',       'Electronics',  1200.00),
('Wireless Headphones', 'Electronics',   150.00),
('Smartphone X12',      'Electronics',   899.00),
('USB-C Hub',           'Electronics',    45.00),
('Running Shoes',       'Apparel',        89.99),
('Winter Jacket',       'Apparel',       129.99),
('Yoga Pants',          'Apparel',        49.99),
('Python Programming',  'Books',          39.99),
('Data Engineering',    'Books',          44.99),
('Machine Learning',    'Books',          49.99);

-- INVENTORY (with reorder levels)
-- reorder_level = minimum stock before restocking alert triggered
INSERT INTO inventory (product_id, quantity, reorder_level) VALUES
(1,  50,  5),   -- Laptop: reorder when below 5
(2, 200, 20),   -- Headphones: reorder when below 20
(3,  75, 10),   -- Smartphone: reorder when below 10
(4, 300, 30),   -- USB-C Hub: reorder when below 30
(5, 150, 15),   -- Running Shoes: reorder when below 15
(6, 100, 10),   -- Winter Jacket: reorder when below 10
(7, 250, 25),   -- Yoga Pants: reorder when below 25
(8, 500, 50),   -- Python Book: reorder when below 50
(9, 400, 40),   -- Data Eng Book: reorder when below 40
(10, 350, 35);  -- ML Book: reorder when below 35

-- ORDERS (15 orders with TIMESTAMP)
INSERT INTO orders (customer_id, order_date, total_amount, order_status) VALUES
(1,  '2024-01-05 09:30:00',  1350.00, 'Delivered'),
(2,  '2024-01-10 14:15:00',   899.00, 'Delivered'),
(3,  '2024-01-15 11:00:00',   219.98, 'Delivered'),
(4,  '2024-02-01 16:45:00',  1245.00, 'Delivered'),
(5,  '2024-02-14 10:20:00',   179.98, 'Shipped'),
(6,  '2024-02-20 13:30:00',    84.98, 'Shipped'),
(7,  '2024-03-01 08:00:00',  1349.99, 'Shipped'),
(8,  '2024-03-10 15:00:00',   194.97, 'Pending'),
(9,  '2024-03-15 12:30:00',   944.99, 'Pending'),
(10, '2024-03-20 09:00:00',   134.97, 'Pending'),
(1,  '2024-04-01 10:00:00',   150.00, 'Delivered'),
(2,  '2024-04-10 14:00:00',    45.00, 'Delivered'),
(3,  '2024-04-15 11:30:00',   899.00, 'Shipped'),
(4,  '2024-04-20 16:00:00',   129.99, 'Shipped'),
(5,  '2024-04-25 09:45:00',    49.99, 'Pending');

-- ORDER ITEMS (with discount and final price)
-- Gold customers get 10% discount
-- Silver customers get 5% discount
-- Bronze customers get 0% discount
INSERT INTO order_items (order_id, product_id, quantity, price_at_purchase, discount_percent, final_price) VALUES
-- Order 1: Alice (Gold - 10% discount)
(1,  1, 1, 1200.00, 10.00, 1080.00),
(1,  2, 1,  150.00, 10.00,  135.00),
-- Order 2: Bob (Silver - 5% discount)
(2,  3, 1,  899.00,  5.00,  854.05),
-- Order 3: Carol (Bronze - 0% discount)
(3,  5, 1,   89.99,  0.00,   89.99),
(3,  7, 1,   49.99,  0.00,   49.99),
(3,  8, 2,   39.99,  0.00,   79.98),
-- Order 4: David (Gold - 10% discount)
(4,  1, 1, 1200.00, 10.00, 1080.00),
(4,  4, 1,   45.00, 10.00,   40.50),
-- Order 5: Emma (Silver - 5% discount)
(5,  6, 1,  129.99,  5.00,  123.49),
(5,  7, 1,   49.99,  5.00,   47.49),
-- Order 6: Frank (Bronze - 0% discount)
(6,  8, 1,   39.99,  0.00,   39.99),
(6,  9, 1,   44.99,  0.00,   44.99),
-- Order 7: Grace (Silver - 5% discount)
(7,  1, 1, 1200.00,  5.00, 1140.00),
(7,  5, 1,   89.99,  5.00,   85.49),
(7,  7, 1,   49.99,  5.00,   47.49),
-- Order 8: Henry (Bronze - 0% discount)
(8,  8, 1,   39.99,  0.00,   39.99),
(8,  9, 1,   44.99,  0.00,   44.99),
(8, 10, 1,   49.99,  0.00,   49.99),
(8,  4, 1,   45.00,  0.00,   45.00),
-- Order 9: Isabel (Gold - 10% discount)
(9,  3, 1,  899.00, 10.00,  809.10),
(9,  5, 1,   89.99, 10.00,   80.99),
-- Order 10: James (Bronze - 0% discount)
(10,  8, 1,  39.99,  0.00,   39.99),
(10,  9, 1,  44.99,  0.00,   44.99),
(10, 10, 1,  49.99,  0.00,   49.99),
-- Order 11: Alice (Gold - 10% discount)
(11, 2, 1,  150.00, 10.00,  135.00),
-- Order 12: Bob (Silver - 5% discount)
(12, 4, 1,   45.00,  5.00,   42.75),
-- Order 13: Carol (Bronze - 0% discount)
(13, 3, 1,  899.00,  0.00,  899.00),
-- Order 14: David (Gold - 10% discount)
(14, 6, 1,  129.99, 10.00,  116.99),
-- Order 15: Emma (Silver - 5% discount)
(15, 7, 1,   49.99,  5.00,   47.49);


-- SECTION 2: BUSINESS KPIs
-- ============================================================

-- KPI 1: Total Revenue from Shipped or Delivered orders
-- Uses final_price to reflect actual revenue after discounts
SELECT
    SUM(oi.final_price) AS total_revenue
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_status IN ('Shipped', 'Delivered');

-- KPI 2: Top 10 Customers by Total Spending
SELECT
    c.customer_id,
    c.full_name,
    c.customer_tier,
    COUNT(DISTINCT o.order_id)  AS total_orders,
    SUM(oi.final_price)         AS total_spent
FROM customers c
JOIN orders o       ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id    = oi.order_id
GROUP BY c.customer_id, c.full_name, c.customer_tier
ORDER BY total_spent DESC
LIMIT 10;

-- KPI 3: Top 5 Best Selling Products by Quantity
SELECT
    p.product_id,
    p.product_name,
    p.category,
    SUM(oi.quantity)    AS total_quantity_sold,
    SUM(oi.final_price) AS total_revenue
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
JOIN orders o       ON oi.order_id  = o.order_id
GROUP BY p.product_id, p.product_name, p.category
ORDER BY total_quantity_sold DESC
LIMIT 5;

-- KPI 4: Monthly Sales Trend
SELECT
    EXTRACT(YEAR  FROM o.order_date)        AS sale_year,
    EXTRACT(MONTH FROM o.order_date)        AS sale_month,
    TO_CHAR(o.order_date, 'Month YYYY')     AS month_name,
    COUNT(DISTINCT o.order_id)              AS total_orders,
    SUM(oi.final_price)                     AS monthly_revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status IN ('Shipped', 'Delivered')
GROUP BY
    EXTRACT(YEAR  FROM o.order_date),
    EXTRACT(MONTH FROM o.order_date),
    TO_CHAR(o.order_date, 'Month YYYY')
ORDER BY sale_year, sale_month;

-- KPI 5: Revenue by Customer Tier
-- Shows how much each tier contributes to total revenue
SELECT
    c.customer_tier,
    COUNT(DISTINCT c.customer_id)   AS total_customers,
    COUNT(DISTINCT o.order_id)      AS total_orders,
    SUM(oi.final_price)             AS total_revenue,
    ROUND(AVG(oi.final_price), 2)   AS avg_order_value
FROM customers c
JOIN orders o       ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id    = oi.order_id
GROUP BY c.customer_tier
ORDER BY total_revenue DESC;


-- SECTION 3: WINDOW FUNCTIONS
-- ============================================================

-- Window Function 1: Sales Rank by Category
WITH product_sales AS (
    SELECT
        p.product_id,
        p.product_name,
        p.category,
        p.price,
        SUM(oi.quantity)    AS total_quantity_sold,
        SUM(oi.final_price) AS total_revenue
    FROM products p
    JOIN order_items oi ON p.product_id = oi.product_id
    GROUP BY p.product_id, p.product_name, p.category, p.price
)
SELECT
    product_id,
    product_name,
    category,
    price,
    total_quantity_sold,
    total_revenue,
    RANK() OVER (
        PARTITION BY category
        ORDER BY total_revenue DESC
    ) AS sales_rank
FROM product_sales
ORDER BY category, sales_rank;

-- Window Function 2: Customer Order Frequency
SELECT
    o.order_id,
    c.full_name,
    c.customer_tier,
    o.order_date                        AS current_order_date,
    o.total_amount,
    LAG(o.order_date) OVER (
        PARTITION BY c.customer_id
        ORDER BY o.order_date
    )                                   AS previous_order_date,
    o.order_date - LAG(o.order_date) OVER (
        PARTITION BY c.customer_id
        ORDER BY o.order_date
    )                                   AS days_since_last_order
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
ORDER BY c.customer_id, o.order_date;

-- Window Function 3: Running Total Revenue
SELECT
    o.order_id,
    o.order_date,
    o.total_amount,
    SUM(o.total_amount) OVER (
        ORDER BY o.order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total_revenue
FROM orders o
WHERE o.order_status IN ('Shipped', 'Delivered')
ORDER BY o.order_date;

-- Window Function 4: Revenue Percentage by Category
WITH product_sales AS (
    SELECT
        p.product_name,
        p.category,
        SUM(oi.final_price) AS total_revenue
    FROM products p
    JOIN order_items oi ON p.product_id = oi.product_id
    GROUP BY p.product_id, p.product_name, p.category
)
SELECT
    product_name,
    category,
    total_revenue,
    ROUND(
        100.0 * total_revenue /
        SUM(total_revenue) OVER (PARTITION BY category), 2
    ) AS revenue_percentage
FROM product_sales
ORDER BY category, total_revenue DESC;


-- SECTION 4: VIEWS
-- ============================================================

-- Query CustomerSalesSummary view
SELECT * FROM CustomerSalesSummary
ORDER BY total_amount_spent DESC;

-- Query LowStockAlert view
SELECT * FROM LowStockAlert
WHERE stock_status != 'SUFFICIENT';

-- Query InventoryAuditHistory view
SELECT * FROM InventoryAuditHistory
LIMIT 10;


-- SECTION 5: STORED PROCEDURE — ProcessNewOrder
-- ============================================================
-- Accepts multiple products via JSON array
-- Handles inventory check, discount calculation,
-- audit logging and customer tier update

DROP PROCEDURE IF EXISTS ProcessNewOrder;

CREATE OR REPLACE PROCEDURE ProcessNewOrder(
    p_customer_id  INT,
    -- JSON array of products: [{"product_id": 1, "quantity": 2}, ...]
    -- Why JSON: Allows passing multiple products in one call
    -- enabling real e-commerce multi-product orders
    p_order_items  JSON
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_order_id       INT;
    v_total_amount   DECIMAL(10,2) := 0;
    v_customer_tier  VARCHAR(10);
    v_discount       DECIMAL(5,2)  := 0;
    v_item           JSON;
    v_product_id     INT;
    v_quantity       INT;
    v_price          DECIMAL(10,2);
    v_final_price    DECIMAL(10,2);
    v_current_stock  INT;
    v_item_total     DECIMAL(10,2);
    v_total_spent    DECIMAL(10,2);

BEGIN
    -- --------------------------------------------------------
    -- STEP 1: GET CUSTOMER TIER FOR DISCOUNT
    -- --------------------------------------------------------
    SELECT customer_tier INTO v_customer_tier
    FROM customers
    WHERE customer_id = p_customer_id;

    -- Assign discount based on customer tier
    -- Why tiered discounts: rewards loyal customers and
    -- incentivizes spending to reach higher tiers
    v_discount := CASE v_customer_tier
        WHEN 'Gold'   THEN 10.00  -- 10% discount for Gold
        WHEN 'Silver' THEN  5.00  -- 5% discount for Silver
        ELSE               0.00   -- No discount for Bronze
    END;

    -- --------------------------------------------------------
    -- STEP 2: VALIDATE ALL PRODUCTS HAVE ENOUGH STOCK
    -- --------------------------------------------------------
    -- Check stock for ALL products BEFORE creating order
    -- Why check all first: avoids partial order creation
    -- where some items succeed but others fail
    FOR v_item IN SELECT * FROM json_array_elements(p_order_items)
    LOOP
        v_product_id := (v_item->>'product_id')::INT;
        v_quantity   := (v_item->>'quantity')::INT;

        SELECT quantity INTO v_current_stock
        FROM inventory
        WHERE product_id = v_product_id
        FOR UPDATE;

        IF v_current_stock < v_quantity THEN
            RAISE EXCEPTION
                'Insufficient stock for product ID %. '
                'Requested: %, Available: %',
                v_product_id, v_quantity, v_current_stock;
        END IF;
    END LOOP;

    -- --------------------------------------------------------
    -- STEP 3: CREATE ORDER HEADER
    -- --------------------------------------------------------
    INSERT INTO orders (customer_id, order_date, total_amount, order_status)
    VALUES (p_customer_id, CURRENT_TIMESTAMP, 0, 'Pending')
    RETURNING order_id INTO v_order_id;

    -- Log order creation in audit table
    INSERT INTO order_audit (
        order_id, customer_id, previous_status,
        new_status, changed_by, notes
    )
    VALUES (
        v_order_id, p_customer_id, NULL,
        'Pending', 'SYSTEM',
        'Order created with ' || json_array_length(p_order_items) || ' items'
    );

    -- --------------------------------------------------------
    -- STEP 4: PROCESS EACH PRODUCT
    -- --------------------------------------------------------
    FOR v_item IN SELECT * FROM json_array_elements(p_order_items)
    LOOP
        v_product_id := (v_item->>'product_id')::INT;
        v_quantity   := (v_item->>'quantity')::INT;

        -- Get current product price
        SELECT price INTO v_price
        FROM products
        WHERE product_id = v_product_id;

        -- Calculate final price after discount
        v_final_price := v_price * v_quantity * (1 - v_discount / 100);
        v_item_total  := v_item_total + v_final_price;

        -- Create order item record
        INSERT INTO order_items (
            order_id, product_id, quantity,
            price_at_purchase, discount_percent, final_price
        )
        VALUES (
            v_order_id, v_product_id, v_quantity,
            v_price, v_discount, v_final_price
        );

        -- Get current stock before update (for audit log)
        SELECT quantity INTO v_current_stock
        FROM inventory
        WHERE product_id = v_product_id;

        -- Reduce inventory
        UPDATE inventory
        SET quantity     = quantity - v_quantity,
            last_updated = CURRENT_TIMESTAMP
        WHERE product_id = v_product_id;

        -- Log inventory change in audit table
        -- Why: provides complete audit trail of stock changes
        INSERT INTO inventory_log (
            product_id, previous_quantity, new_quantity,
            quantity_change, change_reason, order_id, changed_by
        )
        VALUES (
            v_product_id, v_current_stock,
            v_current_stock - v_quantity,
            -v_quantity,
            'ORDER_PLACED', v_order_id, 'SYSTEM'
        );

        v_total_amount := v_total_amount + v_final_price;

    END LOOP;

    -- --------------------------------------------------------
    -- STEP 5: UPDATE ORDER TOTAL
    -- --------------------------------------------------------
    UPDATE orders
    SET total_amount = v_total_amount
    WHERE order_id = v_order_id;

    -- --------------------------------------------------------
    -- STEP 6: UPDATE CUSTOMER TIER BASED ON TOTAL SPENDING
    -- --------------------------------------------------------
    -- Recalculate total spending after this order
    SELECT SUM(oi.final_price) INTO v_total_spent
    FROM order_items oi
    JOIN orders o ON oi.order_id = o.order_id
    WHERE o.customer_id = p_customer_id;

    -- Update tier based on cumulative spending
    UPDATE customers
    SET customer_tier = CASE
        WHEN v_total_spent > 2000 THEN 'Gold'
        WHEN v_total_spent > 500  THEN 'Silver'
        ELSE                           'Bronze'
    END
    WHERE customer_id = p_customer_id;

    -- --------------------------------------------------------
    -- STEP 7: CONFIRM SUCCESS
    -- --------------------------------------------------------
    RAISE NOTICE 'Order processed successfully!';
    RAISE NOTICE 'Order ID       : %', v_order_id;
    RAISE NOTICE 'Customer ID    : %', p_customer_id;
    RAISE NOTICE 'Customer Tier  : %', v_customer_tier;
    RAISE NOTICE 'Discount       : %', v_discount;
    RAISE NOTICE 'Total Amount   : $%', v_total_amount;
    RAISE NOTICE 'Items ordered  : %', json_array_length(p_order_items);

END;
$$;


-- ============================================================
-- TEST STORED PROCEDURE
-- ============================================================

-- Test 1: Valid multi-product order (Gold customer - 10% discount)
CALL ProcessNewOrder(
    1,  -- Alice Johnson (Gold)
    '[
        {"product_id": 1, "quantity": 1},
        {"product_id": 2, "quantity": 2},
        {"product_id": 4, "quantity": 3}
    ]'::JSON
);

-- Verify order created
SELECT * FROM orders ORDER BY order_id DESC LIMIT 1;

-- Verify order items
SELECT * FROM order_items ORDER BY order_item_id DESC LIMIT 3;

-- Verify inventory reduced
SELECT * FROM inventory WHERE product_id IN (1, 2, 4);

-- Verify inventory log
SELECT * FROM InventoryAuditHistory LIMIT 3;

-- Test 2: Invalid order (insufficient stock)
CALL ProcessNewOrder(
    1,
    '[{"product_id": 1, "quantity": 9999}]'::JSON
);
-- Expected: ERROR — Insufficient stock for product ID 1

-- Check low stock alerts
SELECT * FROM LowStockAlert;

-- Check customer tier after orders
SELECT customer_id, full_name, customer_tier
FROM customers
ORDER BY customer_id;