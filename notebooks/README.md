# notebooks — PLANNED SCAFFOLD (Phase 2, Tasks 01-02)

**Status: planned. No notebook in this directory has ever been executed, in a workspace or locally.**

Thin Databricks notebooks (file-format `.py`, `# Databricks` header) capture the parameter contract from the [execution guide](../docs/phase-2/execution-guide.md) and delegate layer logic to `src/transforms/`. They reference `dbutils`, which exists only inside a Databricks session — they are not local entry points and cannot be validated outside the workspace.

| Notebook | Purpose | Execution status |
| :--- | :--- | :--- |
| `staging_to_bronze.py` | Staging-to-Bronze unit (Task 01 scaffold) | PLANNED — never executed |
| `bronze_to_silver.py` | Bronze-to-Silver unit (Task 01 scaffold) | PLANNED — never executed |
| `workspace_readiness.py` | Task 02 readiness: staged synthetic readback, explicit-schema fixture, isolated `task02_` Delta MERGE/replay, import-route probe | AWAITING human workspace run — [checklist](../docs/phase-2/implementation-evidence/task-02-checklist.md) |

Cloud execution evidence (workspace identifier, run IDs, sanitized outputs) is required before any notebook may be described as working. See [submission-evidence.md](../docs/phase-2/submission-evidence.md).
