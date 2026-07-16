# Database Schema - Supernova

## Entity Relationship Diagram (ERD)

```mermaid
erDiagram
    USER ||--o| BRANCH : belongs_to
    PRODUCT ||--|| GLOBAL_STOCK : has
    PRODUCT ||--o{ BRANCH_STOCK : has
    BRANCH ||--o{ BRANCH_STOCK : holds
    BRANCH ||--o{ SALE : processes
    USER ||--o{ SALE : makes
    BRANCH ||--o{ ORDER : receives
    USER ||--o{ ORDER : creates
    ORDER ||--o{ ORDER_ITEM : contains
    PRODUCT ||--o{ ORDER_ITEM : ordered_as
    PRODUCT ||--o{ STOCK_DISTRIBUTION : distributed
    BRANCH ||--o{ STOCK_DISTRIBUTION : receives
    BANNER ||--o| PRODUCT : highlights

    USER {
        int id
        string email
        string password
        string role "OWNER | EMPLOYEE | CUSTOMER"
        int branchId
    }
    PRODUCT {
        int id
        string name
        string description
        decimal price
        string sku
        string image
    }
    BRANCH {
        int id
        string name
        string address
        string phone
    }
    GLOBAL_STOCK {
        int id
        int productId
        int quantity
    }
    BRANCH_STOCK {
        int id
        int branchId
        int productId
        int quantity
    }
    STOCK_DISTRIBUTION {
        int id
        int productId
        int branchId
        int quantity
        string status "PENDING | RECEIVED"
        datetime createdAt
    }
    ORDER {
        int id
        int userId
        int branchId
        decimal totalAmount
        string status
        datetime createdAt
    }
    SALE {
        int id
        int branchId
        int userId
        decimal totalAmount
        datetime transactionDate
    }
```

## Description
- **USER**: Centralized table for all roles. Employees are tied to a specific `branchId`.
- **PRODUCT**: Master catalog of all perfume products.
- **GLOBAL_STOCK**: Single record per product representing warehouse inventory.
- **BRANCH_STOCK**: Inventory per product per branch.
- **STOCK_DISTRIBUTION**: Tracks movement of goods between Global and Branch.
- **ORDER/SALE**: Records of customer buying and point-of-sale transactions.
