---
description: Process for implementing a complex feature in Supernova
---

# Workflow: Create Feature

1. **Analysis**:
   - Read `docs/product.md` and `docs/architecture.md` to understand existing patterns.
   - Check `agent/tasks.md` for related work.

2. **Design**:
   - Identify which modules (Stock, Sales, etc.) are affected.
   - Draft the database schema changes (if any).
   - Propose the change in an `implementation_plan.md` artifact.

3. **Backend Implementation**:
   - Implement logic in small, testable chunks.
   - Ensure stock integrity if the feature involves inventory.

4. **Frontend Implementation**:
   - Build UI components following `docs/coding-standards.md`.
   - Connect to backend using the centralized API client.

5. **Verification**:
   - Test the flow as different roles (Owner vs Employee).
   - Document the results in a `walkthrough.md`.
