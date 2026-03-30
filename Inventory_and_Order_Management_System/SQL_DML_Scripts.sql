-- DML SCRIPT: Inventory and Order Management System
-- Author: Odile
-- Database: PostgreSQL (Neon)
-- Description: Sample data, KPI queries, window functions,
--              views and stored procedures


-- SECTION 1: SAMPLE DATA
-- ============================================================

-- SAMPLE DATA: Inventory and Order Management System
-- Insert realistic sample data for testing and analysis

-- TABLE 1 — CUSTOMERS (10 customers)

INSERT INTO customers (full_name, email, phone, shipping_address) VALUES
('Alice Keza',   'alice.keza@email.com',   '0790075376', 'Kinazi, Ruhango, South'),
('Bob Teta',       'bob.teta@email.com',        '0788567898', 'Ave, Kicukiro, Kigali'),
('Carol Ishimwe',  'carol.ishimwe@email.com',   '0795444337', 'kabeza, Kanombe, Kicukiro'),
('David Bana',     'david.bana@email.com',      '+0781555104', 'kagondo, Niboye, Kicukiro'),
('Emma Ineza',      'emma.ineza@email.com',        '+0795010598', 'Gakinjiro, Gisozi, Gasabo'),
('Frank Ganza',    'frank.ganza@email.com',     '+0788090106', 'ziniya, Gikondo, Kicukiro'),
('Grace Sugi',    'grace.sugi@email.com',     '+0797710107', 'Gatsata, Nyabugogo, Gasabo'),
('Henry Manzi',     'henry.manzi@email.com',      '+0786655108', 'Gatenga, Ngoma, Kicukiro'),
('Isabel Bwiza',   'isabel.bwiza@email.com',    '+0788655109', 'Gisementi, Remera, Gasabo'),
('James Hirwa',  'james.hirwa@email.com',   '+0789456776', 'Amakawa, Jabana, Gasabo');

-- ============================================================
-- TABLE 2 — PRODUCTS (10 products across 3 categories)
-- ============================================================

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

-- ============================================================
-- TABLE 3 — INVENTORY (one record per product)
-- ============================================================

INSERT INTO inventory (product_id, quantity) VALUES
(1,  50),   -- Laptop Pro 15
(2, 200),   -- Wireless Headphones
(3,  75),   -- Smartphone X12
(4, 300),   -- USB-C Hub
(5, 150),   -- Running Shoes
(6, 100),   -- Winter Jacket
(7, 250),   -- Yoga Pants
(8, 500),   -- Python Programming
(9, 400),   -- Data Engineering
(10, 350);  -- Machine Learning

-- ============================================================
-- TABLE 4 — ORDERS (15 orders from various customers)
-- ============================================================

INSERT INTO orders (customer_id, order_date, total_amount, order_status) VALUES
(1,  '2024-01-05',  1350.00, 'Delivered'),
(2,  '2024-01-10',   899.00, 'Delivered'),
(3,  '2024-01-15',   219.98, 'Delivered'),
(4,  '2024-02-01',  1245.00, 'Delivered'),
(5,  '2024-02-14',   179.98, 'Shipped'),
(6,  '2024-02-20',    84.98, 'Shipped'),
(7,  '2024-03-01',  1349.99, 'Shipped'),
(8,  '2024-03-10',   194.97, 'Pending'),
(9,  '2024-03-15',   944.99, 'Pending'),
(10, '2024-03-20',   134.97, 'Pending'),
(1,  '2024-04-01',   150.00, 'Delivered'),
(2,  '2024-04-10',    45.00, 'Delivered'),
(3,  '2024-04-15',   899.00, 'Shipped'),
(4,  '2024-04-20',   129.99, 'Shipped'),
(5,  '2024-04-25',    49.99, 'Pending');

-- ============================================================
-- TABLE 5 — ORDER ITEMS (linking orders to products)
-- ============================================================

INSERT INTO order_items (order_id, product_id, quantity, price_at_purchase) VALUES
-- Order 1: Alice bought Laptop + Headphones
(1,  1, 1, 1200.00),
(1,  2, 1,  150.00),

-- Order 2: Bob bought Smartphone
(2,  3, 1,  899.00),

-- Order 3: Carol bought Running Shoes + Yoga Pants
(3,  5, 1,   89.99),
(3,  7, 1,   49.99),
(3,  8, 2,   39.99),

-- Order 4: David bought Laptop + USB-C Hub
(4,  1, 1, 1200.00),
(4,  4, 1,   45.00),

-- Order 5: Emma bought Winter Jacket + Yoga Pants
(5,  6, 1,  129.99),
(5,  7, 1,   49.99),

-- Order 6: Frank bought 2 Books
(6,  8, 1,   39.99),
(6,  9, 1,   44.99),

-- Order 7: Grace bought Laptop + Running Shoes
(7,  1, 1, 1200.00),
(7,  5, 1,   89.99),
(7,  7, 1,   49.99),

-- Order 8: Henry bought 3 Books
(8,  8, 1,   39.99),
(8,  9, 1,   44.99),
(8, 10, 1,   49.99),
(8,  4, 1,   45.00),

-- Order 9: Isabel bought Smartphone + Running Shoes
(9,  3, 1,  899.00),
(9,  5, 1,   89.99),

-- Order 10: James bought 3 Books
(10,  8, 1,  39.99),
(10,  9, 1,  44.99),
(10, 10, 1,  49.99),

-- Order 11: Alice bought Headphones again
(11, 2, 1,  150.00),

-- Order 12: Bob bought USB-C Hub
(12, 4, 1,   45.00),

-- Order 13: Carol bought Smartphone
(13, 3, 1,  899.00),

-- Order 14: David bought Winter Jacket
(14, 6, 1,  129.99),

-- Order 15: Emma bought Yoga Pants
(15, 7, 1,   49.99);

-- ============================================================
-- VERIFY — CHECK DATA WAS INSERTED
-- ============================================================

SELECT 'customers'  AS table_name, COUNT(*) AS row_count FROM customers
UNION ALL
SELECT 'products',   COUNT(*) FROM products
UNION ALL
SELECT 'inventory',  COUNT(*) FROM inventory
UNION ALL
SELECT 'orders',     COUNT(*) FROM orders
UNION ALL
SELECT 'order_items',COUNT(*) FROM order_items;


-- SECTION 2: BUSINESS KPIs
-- ============================================================
-- KPI 1 — TOTAL REVENUE
-- Calculate total revenue from Shipped or Delivered orders only
-- Pending orders are excluded — payment not yet confirmed

SELECT 
   SUM(oi.quantity * oi.price_at_purchase) AS total_revenue
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_status IN ('Shipped', 'Delivered');

-- KPI 2 — TOP 10 CUSTOMERS BY TOTAL SPENDING
-- Find the most valuable customers based on total amount spent
-- Includes all order statuses

SELECT
   c.customer_id,
   c.full_name,
   c.email,
   COUNT(DISTINCT o.order_id)              AS total_orders,
   SUM(oi.quantity * oi.price_at_purchase) AS total_spent
FROM customers c
JOIN orders o      ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY
   c.customer_id,
   c.full_name,
   c.email
ORDER BY total_spent DESC
LIMIT 10;

-- KPI 3 — TOP 5 BEST SELLING PRODUCTS BY QUANTITY
-- Find the most popular products based on total quantity sold
SELECT
	p.product_id,
	p.product_name,
	p.category,
	p.price,
	SUM(oi.quantity)                         AS total_quantity_sold,
	SUM(oi.quantity * oi.price_at_purchase)  AS totsl_revenue
	FROM products p
	JOIN order_items oi ON p.product_id = oi.product_id
	JOIN orders o       ON oi.order_id = o.order_id
	GROUP BY
		P.product_id,
		p.product_name,
		p.category,
		p.price
	ORDER BY total_quantity_sold DESC
	LIMIT 5;

	-- KPI 4 — MONTHLY SALES TREND
-- Show total sales revenue for each month
-- Helps identify peak and slow sales periods

SELECT 
	-- Extract year and month from order date
	EXTRACT(YEAR FROM o.order_date) AS sale_year,
	EXTRACT(MONTH FROM o.order_date) AS sale_month,

	-- Format as readable month name
	TO_CHAR(o.order_date, 'Month YYYY') AS month_name,

	 -- Count orders and calculate revenue
    COUNT(DISTINCT o.order_id)              AS total_orders,
    SUM(oi.quantity * oi.price_at_purchase) AS monthly_revenue

FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status IN ('Shipped', 'Delivered')
GROUP BY
    EXTRACT(YEAR  FROM o.order_date),
    EXTRACT(MONTH FROM o.order_date),
    TO_CHAR(o.order_date, 'Month YYYY')
ORDER BY
    sale_year,
    sale_month;

-- SECTION 3: WINDOW FUNCTIONS
-- ============================================================

-- WINDOW FUNCTION 1 — SALES RANK BY CATEGORY
-- Rank products by total sales revenue within each category
-- #1 = highest revenue in that category

WITH product_sales AS (
    -- Step 1: Calculate total sales per product
    SELECT
        p.product_id,
        p.product_name,
        p.category,
        p.price,
        SUM(oi.quantity)                        AS total_quantity_sold,
        SUM(oi.quantity * oi.price_at_purchase) AS total_revenue
    FROM products p
    JOIN order_items oi ON p.product_id = oi.product_id
    GROUP BY
        p.product_id,
        p.product_name,
        p.category,
        p.price
)

-- Step 2: Rank products within each category
SELECT
    product_id,
    product_name,
    category,
    price,
    total_quantity_sold,
    total_revenue,

    -- RANK() assigns rank within each category
    -- PARTITION BY category → restart ranking for each category
    -- ORDER BY total_revenue DESC → highest revenue = rank 1
    RANK() OVER (
        PARTITION BY category
        ORDER BY total_revenue DESC
    ) AS sales_rank

FROM product_sales
ORDER BY category, sales_rank;


-- ============================================================
-- WINDOW FUNCTION 2 — CUSTOMER ORDER FREQUENCY
-- ============================================================
-- Show each order alongside the customer's previous order date
-- Helps analyze how frequently customers return to buy

SELECT
    o.order_id,
    c.customer_id,
    c.full_name,
    o.order_date                        AS current_order_date,
    o.total_amount,
    o.order_status,

    -- LAG() looks at the PREVIOUS row for the same customer
    -- PARTITION BY customer_id → only look at same customer's orders
    -- ORDER BY order_date → ordered by date so previous = earlier order
    LAG(o.order_date) OVER (
        PARTITION BY c.customer_id
        ORDER BY o.order_date
    ) AS previous_order_date,

    -- Calculate days between current and previous order
    -- If no previous order → NULL (first time customer)
    o.order_date - LAG(o.order_date) OVER (
        PARTITION BY c.customer_id
        ORDER BY o.order_date
    ) AS days_since_last_order

FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
ORDER BY c.customer_id, o.order_date;




-- SECTION 4: VIEW — CustomerSalesSummary
-- ============================================================

-- VIEW — CustomerSalesSummary
-- This view pre-calculates total spending per customer

-- Drop view if it already exists
DROP VIEW IF EXISTS CustomerSalesSummary;

--Create the view
CREATE VIEW CustomerSalesSummary AS
SELECT
	c.customer_id,
	c.full_name,
	c.email,
	c.phone,

	--Count total number of orders per customer
	COUNT(DISTINCT o.order_id)					AS total_orders,
	--Sum of all items purchsed
	SUM(oi.quantity)							AS total_items_purchase,
	--Total amount spent across all orders
	SUM(oi.quantity * oi.price_at_purchase)		AS total_amount_spent,
	--Average order value
	ROUND(
		AVG(oi.quantity * oi.price_at_purchase), 2
	)											AS avg_order_date,
	--Date of first order
	MIN(o.order_date)							AS first_order_date,
	--Date of most recent order
	MAX(o.order_date)							AS last_order_date

FROM customers c
JOIN orders o		ON c.customer_id = o.customer_id
JOIN order_items oi	ON o.order_id = oi.order_id
GROUP BY
	c.customer_id,
	c.full_name,
	c.email,
	c.phone;

--Query 1: see all custoner summaries
SELECT* FROM CustomerSalesSummary
ORDER BY total_amount_spent DESC;

--Query 2: find top spenders easily
SELECT full_name, total_amount_spent
FROM CustomerSalesSummary
WHERE total_amount_spent > 1000
ORDER BY total_amount_spent DESC;

-- Query 3: find loyal customers (more than 1 order)
SELECT full_name, total_orders, total_amount_spent
FROM CustomerSalesSummary
WHERE total_orders > 1
ORDER BY total_orders DESC;


-- STORED PROCEDURE — ProcessNewOrder
-- A stored procedure is a saved set of SQL statements
-- that can be executed with a single call
-- Drop procedure if it already exists

DROP PROCEDURE IF EXISTS ProcessNewOrder;

-- Create the stored procedure
CREATE OR REPLACE PROCEDURE ProcessNewOrder(
    p_customer_id  INT,     -- Customer placing the order
    p_product_id   INT,     -- Product being ordered
    p_quantity     INT      -- Quantity requested
)
LANGUAGE plpgsql            -- PostgreSQL procedural language
AS $$
DECLARE
    -- Variables to store values during execution
    v_current_stock  INT;           -- current stock level
    v_product_price  DECIMAL(10,2); -- product price
    v_total_amount   DECIMAL(10,2); -- total order amount
    v_new_order_id   INT;           -- newly created order ID

BEGIN
    -- --------------------------------------------------------
    -- STEP 1: CHECK CURRENT STOCK LEVEL
    -- --------------------------------------------------------
    -- Fetch current stock for the requested product
    -- FOR UPDATE locks the row to prevent other transactions
    -- from changing stock while we are processing
    SELECT quantity
    INTO v_current_stock
    FROM inventory
    WHERE product_id = p_product_id
    FOR UPDATE;

    -- --------------------------------------------------------
    -- STEP 2: CHECK IF ENOUGH STOCK EXISTS
    -- --------------------------------------------------------
    IF v_current_stock < p_quantity THEN
        -- Not enough stock — raise an error
        -- ROLLBACK happens automatically when exception is raised
        RAISE EXCEPTION
            'Insufficient stock! Requested: %, Available: %',
            p_quantity, v_current_stock;
    END IF;

    -- --------------------------------------------------------
    -- STEP 3: GET PRODUCT PRICE
    -- --------------------------------------------------------
    SELECT price
    INTO v_product_price
    FROM products
    WHERE product_id = p_product_id;

    -- Calculate total order amount
    v_total_amount := p_quantity * v_product_price;

    -- --------------------------------------------------------
    -- STEP 4: REDUCE INVENTORY
    -- --------------------------------------------------------
    -- Subtract the ordered quantity from current stock
    UPDATE inventory
    SET quantity = quantity - p_quantity
    WHERE product_id = p_product_id;

    -- --------------------------------------------------------
    -- STEP 5: CREATE NEW ORDER
    -- --------------------------------------------------------
    -- Insert a new record in orders table
    -- RETURNING order_id captures the auto-generated ID
    INSERT INTO orders (customer_id, order_date, total_amount, order_status)
    VALUES (p_customer_id, CURRENT_DATE, v_total_amount, 'Pending')
    RETURNING order_id INTO v_new_order_id;

    -- --------------------------------------------------------
    -- STEP 6: CREATE ORDER ITEM
    -- --------------------------------------------------------
    -- Insert a new record in order_items table
    -- Store price_at_purchase to preserve historical price
    INSERT INTO order_items (order_id, product_id, quantity, price_at_purchase)
    VALUES (v_new_order_id, p_product_id, p_quantity, v_product_price);

    -- --------------------------------------------------------
    -- STEP 7: CONFIRM SUCCESS
    -- --------------------------------------------------------
    RAISE NOTICE 'Order processed successfully!';
    RAISE NOTICE 'Order ID      : %', v_new_order_id;
    RAISE NOTICE 'Customer ID   : %', p_customer_id;
    RAISE NOTICE 'Product ID    : %', p_product_id;
    RAISE NOTICE 'Quantity      : %', p_quantity;
    RAISE NOTICE 'Total Amount  : $%', v_total_amount;
    RAISE NOTICE 'Stock Left    : %', v_current_stock - p_quantity;

END;
$$;

-- ============================================================
-- HOW TO CALL THE STORED PROCEDURE
-- ============================================================

-- Test 1 — Valid order (enough stock)
-- Customer 1 orders 2 units of Product 1 (Laptop)
CALL ProcessNewOrder(1, 1, 2);

-- Verify order was created
SELECT * FROM orders ORDER BY order_id DESC LIMIT 1;

-- Verify inventory was reduced
SELECT * FROM inventory WHERE product_id = 1;

-- Verify order item was created
SELECT * FROM order_items ORDER BY order_item_id DESC LIMIT 1;

-- Test 2 — Invalid order (not enough stock)
-- Customer 1 orders 1000 units of Product 1 (only 48 left)
CALL ProcessNewOrder(1, 1, 1000);
-- Expected: ERROR — Insufficient stock! Requested: 1000, Available: 48

-- ============================================================
-- VERIFY EVERYTHING USING THE VIEW
-- ============================================================

-- Check customer summary after new orders
SELECT * FROM CustomerSalesSummary
ORDER BY total_amount_spent DESC;


	
