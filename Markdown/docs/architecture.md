# System Architecture - Supernova

## Tech Stack
- **Frontend**: [Next.js](https://nextjs.org/) (App Router, TypeScript, Tailwind CSS)
- **Backend**: [NestJS](https://nestjs.com/) (TypeScript, TypeORM)
- **Database**: [MySQL](https://www.mysql.com/)
- **Authentication**: JWT (JSON Web Token) with Passport.js strategies

## Backend Structure (`backend/src`)
The backend follows a modular architecture typical of NestJS:
- `module.ts`: Defines the module and its dependencies.
- `controller.ts`: Handles incoming HTTP requests and routes them to services.
- `service.ts`: Contains the core business logic.
- `entity.ts`: Defines the database schema using TypeORM decorators.
- `dto/`: Data Transfer Objects for input validation.

## Frontend Structure (`frontend/src`)
- `app/`: Next.js App Router for page definitions.
- `components/`: Reusable UI components (Admin sidebar, Sales charts, etc.).
- `lib/api.ts`: Centralized Axios configuration for backend communication.

## Core System Flows

### Stock Distribution Flow
1. **Creation**: Owner initiates distribution from Global Stock to a Branch.
2. **Pending State**: Global Stock is deducted; `StockDistribution` record created with `PENDING` status.
3. **Confirmation**: Branch Employee confirms receipt; Branch Stock increases, status changes to `RECEIVED`.

### Transactional Flow (POS/Order)
1. **Selection**: User selects products.
2. **Atomic Validation**: Backend checks stock availability and product pricing during checkout.
3. **Execution**:
   - Stock is deducted from Branch Stock.
   - Sale/Order record is created.
   - Transactional consistency is maintained to prevent overselling.
