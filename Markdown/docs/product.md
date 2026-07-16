# Product Documentation - Supernova Inventory

## Vision
Supernova is a centralized Point of Sale (POS) and Supply Chain Management system designed specifically for a multi-branch perfume retail business. It aims to streamline operations from a central warehouse to individual retail branches, providing real-time visibility and operational efficiency.

## Core Objectives
1. **Centralized Inventory Control**: Manage global stock and handle distribution to branches.
2. **Multi-Branch Operations**: Support different branches with independent stock and sales tracking.
3. **Role-Based Management**: Clear separation of duties between Owners, Employees, and Customers.
4. **Data-Driven Insights**: Provide accurate sales reporting and performance monitoring.

## User Roles

### 1. Owner (Administrator)
The decision-maker with full system access.
- **Master Data Management**: Products, branches, and user accounts.
- **Stock Control**: Manages global warehouse stock and distribution logic.
- **Analytics**: Access to aggregated reports and per-branch performance metrics.

### 2. Employee (Branch Staff)
Operational staff tied to a specific branch.
- **Point of Sale**: Process customer transactions at the branch.
- **Stock Management**: Receive incoming stock from the central warehouse.
- **Monitoring**: Real-time view of branch-specific stock levels and sales history.

### 3. Customer
The end-user of the retail service.
- **Catalog Browsing**: View available products across branches.
- **Digital Ordering**: Create orders through the platform.
- **Order History**: Track past purchases and current order status.

## Major Modules
- **Auth**: Secure JWT-based authentication and role-based access control.
- **Product**: Central repository for perfume items, pricing, and categories.
- **Stock**: The heart of the system, managing Global Stock, Branch Stock, and pending distributions.
- **Sales**: Records every transaction for reporting and stock deduction.
- **Order**: Customer-facing ordering workflow with atomic stock validation.
- **Branch**: Management of physical retail locations.
