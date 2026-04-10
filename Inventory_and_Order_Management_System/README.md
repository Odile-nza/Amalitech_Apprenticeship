# Inventory and Order Management System

A PostgreSQL database project designed for an e-commerce company. The system manages customers, products, inventory and orders using a normalized relational database schema in Third Normal Form (3NF) with audit logging, customer tiering and performance optimization.

---

## Project Structure

```
Inventory_and_Order_Management_System/
├── ERD_Inventory_Order_MS.pdf    ERD diagram of the database schema
├── SQL_DDL_Script.sql            CREATE TABLE statements with constraints and indexes
└── SQL_DML_Scripts.sql           Sample data, KPI queries, window functions,
                                  views and stored procedures
```

---

## Database Schema

The system contains 7 tables:

| Table | Description |
|---|---|
| customers | Stores customer information including loyalty tier (Bronze/Silver/Gold) |
| products | Stores product details including category and price |
| inventory | Tracks current stock level, reorder level and last updated timestamp |
| orders | Stores order header information with exact TIMESTAMP |
| order_items | Bridge table linking orders to multiple products with discount and final price |
| inventory_log | Audit table tracking every stock change with reason and timestamp |
| order_audit | Audit table tracking every order status change |

### Relationships

- One customer can have many orders (One-to-Many)
- One order can have many order items (One-to-Many)
- One product can appear in many orders (Many-to-Many via order_items)
- One product has one inventory record (One-to-One)
- One product can have many inventory log entries (One-to-Many)
- One order can have many audit entries (One-to-Many)

---

## Key Design Decisions

### TIMESTAMP instead of DATE
Order date uses `TIMESTAMP` to capture the exact time of each order — essential for time-based analytics and auditing.

### Audit Tables
Two audit tables track the complete history of changes:
- `inventory_log` — records every stock change including reason, previous and new quantity
- `order_audit` — records every order status change with timestamp

### Customer Tiering
Customers are automatically classified into three tiers based on cumulative spending:
- Bronze — spending below $500
- Silver — spending between $500 and $2,000
- Gold — spending above $2,000

### Bulk Discounts
Discounts are applied automatically based on customer tier:
- Gold → 10% discount
- Silver → 5% discount
- Bronze → no discount

### Performance Indexes
Seven custom indexes are defined on frequently queried columns to optimize query performance:
- `idx_orders_customer_id`
- `idx_order_items_order_id`
- `idx_order_items_product_id`
- `idx_inventory_product_id`
- `idx_inventory_log_product_id`
- `idx_orders_order_date`
- `idx_customers_tier`

---

## SQL Scripts

### DDL Script
Contains all CREATE TABLE statements with:
- Primary key and foreign key constraints
- NOT NULL and CHECK constraints for data integrity
- TIMESTAMP for precise order tracking
- reorder_level column for automated stock alerts
- 7 custom performance indexes

### DML Script
Organized into 5 sections:

**Section 1 — Sample Data**
- 10 customers with Bronze, Silver and Gold tiers
- 10 products across 3 categories (Electronics, Apparel, Books)
- Inventory records with reorder levels
- 15 orders with exact timestamps
- 29 order items with discounts and final prices

**Section 2 — Business KPIs**
- Total revenue from Shipped and Delivered orders
- Top 10 customers by total spending
- Top 5 best selling products by quantity
- Monthly sales trend
- Revenue by customer tier

**Section 3 — Window Functions**
- Sales rank by product category using RANK()
- Customer order frequency using LAG()
- Running total revenue
- Revenue percentage by category

**Section 4 — Views**
- `CustomerSalesSummary` — pre-calculates spending per customer including tier
- `LowStockAlert` — shows products below reorder level
- `InventoryAuditHistory` — shows complete stock change history

**Section 5 — Stored Procedure**
- `ProcessNewOrder` — accepts multiple products via JSON array
- Validates stock for all products before creating order
- Applies tier-based discount automatically
- Creates order and order items in one transaction
- Logs every inventory change to inventory_log
- Logs order creation to order_audit
- Updates customer tier based on cumulative spending

---

## Key Findings

### Revenue by Customer Tier
| Tier | Customers | Total Revenue | Avg Order Value |
|---|---|---|---|
| Gold | 3 | $3,477.58 | $434.70 |
| Silver | 3 | $2,388.25 | $298.53 |
| Bronze | 4 | $1,518.88 | $116.84 |

### Revenue by Category
| Category | Top Product | Revenue Share |
|---|---|---|
| Electronics | Laptop Pro 15 | 52.71% |
| Books | Python Programming | 45.98% |
| Apparel | Running Shoes | 37.20% |

### Stored Procedure Test Results
- Valid order (Gold customer, 3 products): $1,471.50 with 10% discount applied
- Invalid order (insufficient stock): Error raised and transaction rolled back

---

## How to Run

### Requirements
- PostgreSQL database (local or cloud e.g. Neon)
- pgAdmin or any PostgreSQL client

### Steps
1. Create a new database
2. Run `SQL_DDL_Script.sql` to create all tables, views and indexes
3. Run `SQL_DML_Scripts.sql` section by section:
   - Section 1 → insert sample data
   - Section 2 → run KPI queries
   - Section 3 → run window functions
   - Section 4 → query views
   - Section 5 → create and test stored procedure

### Test the Stored Procedure
```sql
-- Multi-product order with automatic discount
CALL ProcessNewOrder(
    1,
    '[
        {"product_id": 1, "quantity": 1},
        {"product_id": 2, "quantity": 2},
        {"product_id": 4, "quantity": 3}
    ]'::JSON
);
```

---

## Tools Used

| Tool | Purpose |
|---|---|
| PostgreSQL | Relational database management system |
| pgAdmin 4 | Database administration and query execution |
| Neon | Cloud hosted PostgreSQL database |
| dbdiagram.io | ERD diagram design |
| Git | Version control |

---

## Author

Odile Nzambazamariya — AmaliTech Data Engineering Apprentice