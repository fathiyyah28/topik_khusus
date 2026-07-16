---
description: Standard procedure for fixing bugs in Supernova
---

# Workflow: Bugfix

1. **Reproduction**:
   - Identify the failed endpoint or UI component.
   - Use `list_dir` and `view_file` to examine the suspect code.
   - Try to reproduce the error locally.

2. **Root Cause Analysis**:
   - Check terminal/browser console logs.
   - Verify if it's a logic error, a type mismatch, or a database constraint violation.

3. **Implementation**:
   - Fix the code following `docs/coding-standards.md`.
   - If it's a stock-related bug, double-check that `StockService` logic is preserved.

4. **Verification**:
   - Re-run the flow that caused the bug.
   - Check for side effects in related modules (e.g., did fixing a sale bug break stock count?).
   - Document the fix.
