# Coding Standards

## General Guidelines
- **Language**: All code must be written in TypeScript.
- **Style**: Follow standard Prettier and ESLint configurations.
- **Indentation**: 2 spaces.

## Naming Conventions
- **Classes**: `PascalCase` (e.g., `ProductService`).
- **Files**: `kebab-case.suffix.ts` (e.g., `create-product.dto.ts`).
- **Variables/Functions**: `camelCase`.
- **Database Tables/Columns**: `camelCase` (TypeORM default) or `snake_case` if explicitly mapped.

## Backend Standards (NestJS)
- **Validation**: Every POST/PUT request must use a DTO with `class-validator` decorators.
- **Dependency Injection**: Always use DI for services and repositories.
- **Exception Filters**: Use built-in NestJS `HttpException` classes for standard errors.

## API Response Format
Success:
```json
{
  "statusCode": 200,
  "message": "Success",
  "data": { ... }
}
```

Error:
```json
{
  "statusCode": 400,
  "message": "Bad Request",
  "error": "Detailed error message"
}
```

## Frontend Standards (Next.js/React)
- **Component Types**: Use Functional Components with Hooks.
- **State Management**: Use React Hooks (`useState`, `useContext`) for local/global state.
- **API Calls**: All API calls must go through the centralized `axios` instance in `lib/api.ts`.
