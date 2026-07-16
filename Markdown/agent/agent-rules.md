# Agent Rules - Supernova

## Purpose
This document provides guidelines for AI agents interacting with the Supernova codebase to ensure consistency, security, and integrity.

## General Principles
- **Read Before Write**: Always read existing logic, especially in `StockService`, before making modifications.
- **Maintain Consistency**: Follow the standards defined in `docs/coding-standards.md`.
- **Absolute Paths**: When using tools, always prefer absolute paths to avoid ambiguity.
- **Validation**: Ensure all new API endpoints have corresponding DTOs and validation.

## Tool Usage
- `run_command`: Use for building, testing, and migrations. Avoid destructive commands.
- `edit_file`: Prefer surgical edits over full-file overwrites for existing logic.
- `search_web`: Use for clarifying library-specific issues (e.g., NestJS or TypeORM).

## Prohibited Actions
- **No Manual Stock Edits**: Never bypass `StockService` logic to manually update stock values in the database.
- **No Direct Schema Mutation**: Always use TypeORM entities or migrations for database changes.
- **No Bypassing Guards**: Do not disable `JwtGuard` or `RolesGuard` for convenience.
