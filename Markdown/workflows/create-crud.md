---
description: How to create a new CRUD module in Supernova
---

# Workflow: Create CRUD

1. **Entity Definition**:
   - Create a new folder in `backend/src/` for the module.
   - Define the `*.entity.ts` file with TypeORM decorators.
   - Register the entity in `app.module.ts`.

2. **DTO Creation**:
   - Create `dto/create-x.dto.ts` and `dto/update-x.dto.ts`.
   - Use `class-validator` for all fields.

3. **Service Implementation**:
   - Generate service using Nest CLI: `nest g s [name]`.
   - Implement basic CRUD methods (findAll, findOne, create, update, remove).

4. **Controller Routing**:
   - Generate controller using Nest CLI: `nest g co [name]`.
   - Add appropriate `@Get()`, `@Post()`, `@Patch()`, `@Delete()` decorators.
   - Apply `@UseGuards(JwtGuard, RolesGuard)` as needed.

5. **Frontend Integration**:
   - Add API methods in `frontend/src/lib/api.ts` (if applicable).
   - Create management pages in `frontend/src/app/admin/[name]`.
   - Use standardized table/form components.
