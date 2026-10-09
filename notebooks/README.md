# notebooks — PLANNED SCAFFOLD (Phase 2, Task 01)

**Status: planned. No notebook in this directory has ever been executed, in a workspace or locally.**

Thin Databricks notebooks (file-format `.py`, `# Databricks` header) will only capture the parameter contract from the [execution guide](../docs/phase-2/execution-guide.md) and delegate to `src/transforms/`. They reference `dbutils`, which exists only inside a Databricks session — they are not local entry points and cannot be validated outside the workspace.

| Notebook | Planned layer |
| :--- | :--- |
| `staging_to_bronze.py` | Staging-to-Bronze unit |
| `bronze_to_silver.py` | Bronze-to-Silver unit |

Cloud execution evidence (workspace identifier, run IDs, sanitized outputs) is required before any notebook may be described as working. See [submission-evidence.md](../docs/phase-2/submission-evidence.md).
