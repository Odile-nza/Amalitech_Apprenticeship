# Inventory and Order Management System

A PostgreSQL database project designed for an e-commerce company. The system manages customers, products, inventory and orders using a normalized relational database schema.

---

## Project Objectives

- Design a normalized relational database schema in Third Normal Form (3NF)
- Implement SQL Data Definition Language (DDL) scripts to create tables, relationships and constraints
- Write advanced SQL queries including joins, aggregations and window functions
- Optimize performance using views and stored procedures

---

## Database Schema

The system contains 5 tables:

| Table | Description |
|---|---|
| customers | Stores customer personal and shipping information |
| products | Stores product details including category and price |
| inventory | Tracks current stock level for each product |
| orders | Stores order header information per customer |
| order_items | Bridge table linking orders and products |

### Relationships

- One customer can have many orders (One-to-Many)
- One order can have many order items (One-to-Many)
- One product can appear in many orders (Many-to-Many via order_items)
- One product has one inventory record (One-to-One)

---

## Project Structure

```
Inventory_and_Order_Management_System/
├── ERD_Inventory_Order_MS.pdf    ERD diagram of the database schema
├── SQL_DDL_Script.sql            CREATE TABLE statements with constraints
└── SQL_DML_Scripts.sql           Sample data, KPI queries, window functions, views and stored procedures
```

---

## SQL Scripts

### DDL Script
Contains all CREATE TABLE statements with:
- Primary key constraints
- Foreign key constraints
- NOT NULL constraints
- CHECK constraints for data integrity

### DML Script
Organized into 5 sections:

**Section 1 - Sample Data**
- 10 customers
- 10 products across 3 categories (Electronics, Apparel, Books)
- Inventory records for each product
- 15 orders with various statuses
- 29 order items

**Section 2 - Business KPIs**
- Total revenue from Shipped and Delivered orders
- Top 10 customers by total spending
- Top 5 best selling products by quantity
- Monthly sales trend

**Section 3 - Window Functions**
- Sales rank by product category using RANK()
- Customer order frequency using LAG()
- Running total revenue
- Revenue percentage by category

**Section 4 - View**
- CustomerSalesSummary view pre-calculating total spending per customer

**Section 5 - Stored Procedure**
- ProcessNewOrder procedure handling stock validation, inventory reduction and order creation within a transaction

---

## How to Run

**Requirements**
- PostgreSQL database (local or cloud e.g. Neon)
- pgAdmin or any PostgreSQL client

**Steps**
1. Create a new database
2. Run SQL_DDL_Script.sql to create all tables
3. Run SQL_DML_Scripts.sql to insert data and execute queries

---

## Key Findings

- Electronics category generates the highest total revenue
- Laptop Pro 15 is the best selling product by revenue
- Alice Johnson is the top spending customer
- January recorded the highest monthly revenue

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

Odile — AmaliTech Data Engineering Apprentice