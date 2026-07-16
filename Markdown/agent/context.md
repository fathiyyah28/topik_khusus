# Project Context - Supernova

## Overview
Supernova is a multi-branch POS and Inventory system built with NestJS and Next.js.

## Key Entities
- **User**: Authentication and authorization.
- **Product**: Goods being sold.
- **Branch**: Retail locations.
- **GlobalStock**: Warehouse inventory.
- **BranchStock**: Retail inventory.
- **Order/Sale**: Transactions.

## Critical Logic
The system's most critical logic resides in the `StockModule`, specifically handling how stock moves from global warehouse to branches and how it's deducted during a sale.

## Technical Debt / Observations
- **Concurrency**: Basic checks are in place, but full DB transactions for complex order flows are a priority for enhancement.
- **Frontend Feedback**: Loading states and error messaging could be more robust.
