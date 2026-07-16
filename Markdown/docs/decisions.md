# Architectural Decisions (ADR)

## ADR 001: Use of Atomic Stock Validation
- **Status**: Accepted
- **Context**: In a multi-branch retail environment, overselling must be prevented at all costs.
- **Decision**: Stock deduction happens immediately upon order creation in a single database operation or transaction.
- **Consequences**: Provides high data integrity but requires careful transaction handling in the backend.

## ADR 002: Modular NestJS Backend
- **Status**: Accepted
- **Context**: The project has distinct domains (Stock, Sales, Auth).
- **Decision**: Organize the backend into feature-based modules.
- **Consequences**: Enhances maintainability and allows independent scaling of features.

## ADR 003: JWT-based Authentication
- **Status**: Accepted
- **Context**: Need a stateless authentication method for a web-based POS.
- **Decision**: Use JSON Web Tokens stored in HTTP-only cookies (recommended) or localized browser storage.
- **Consequences**: Simple to implement and scale across multiple frontend clients if needed.

## ADR 004: Separate Global and Branch Stock
- **Status**: Accepted
- **Context**: Distinguishing between warehouse inventory and shelf inventory is critical for retail.
- **Decision**: Implement two separate entities (`GlobalStock` and `BranchStock`) with a `StockDistribution` bridge.
- **Consequences**: More complex logic for distribution but accurately reflects real-world operations.
