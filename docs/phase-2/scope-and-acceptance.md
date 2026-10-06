# Scope and acceptance

Implement a bounded batch pipeline rather than a continuously running service. Source acquisition may run locally if workspace networking blocks a publisher. Record parsing, Bronze and Silver processing, Delta writes and acceptance runs must execute in cloud PySpark.

| Requirement | Implementation target | Acceptance evidence |
| :--- | :--- | :--- |
| Cloud workspace | Databricks Free Edition; observed catalog, schemas and volume | Sanitized runtime and workspace readiness record |
| Version control | PySpark modules and thin notebooks committed through feature branches | Repository history, reviewed pull requests and reproducible commit |
| Data dictionary | Every Bronze and Silver column, Spark type, nullability, grain and logical key | Reviewed dictionary consistent with code and table descriptions |
| Explicit input contracts | Source-specific StructType and StructField definitions before each Spark file read | Reader code and incompatible-schema tests; no schema inference |
| Casting | Checked dates, UTC timestamps, finite numbers and validated whole-number counts | Valid rows and reason-coded rejects |
| Per-record metadata | Non-null load_timestamp in every Bronze and Silver table | Null checks; unchanged replay preserves existing timestamps |
| Idempotency | Conditional MERGE INTO; deterministic keys and payload hashes | Second execution inserts and updates zero Silver rows |
| Backfills | Explicit batch, source, path and optional publication window | Historical raw-to-Bronze and Bronze-to-Silver replay evidence |
| Drift | File preflight plus quarantine for unsafe schema or row changes | Added-column, changed-type, corrupt-file and valid-file isolation tests |
| Operational tables | Runs, processing units, file inventory and quarantine | Successful, no-op, partial and failed run records |
| Audit metrics | Layer, parameters, file/table, start/end, status and actual inserts/updates | Logs reconciled with attributable Delta write versions |
| Execution guide | Tested parameters, prerequisites and incremental/backfill procedures | A second operator follows the guide from the released commit |

The complete original baseline is acquired and processed; a representative sample run is a development check. Sources counted toward the full-load size must feed useful Silver tables. Every original archive is retained; CooperBench result and evaluation members provide its analytical records. Unreviewed trace content is restricted, not made public to increase row counts.

Phase 2 does not require Gold transformations, dashboard construction, paid inference or rerunning CooperBench experiments. Do not add those to the acceptance scope.
