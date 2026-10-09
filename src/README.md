# src — PLANNED SCAFFOLD (Phase 2, Task 01)

**Status: planned skeleton. Nothing in this directory is implemented, tested or executed.**

No module here downloads data, uploads bytes, reads a file with Spark or writes a table. Every function raises `NotImplementedError` until its Phase 2 task is built and evidenced.

| Path | Planned purpose | Specification |
| :--- | :--- | :--- |
| `collector/acquire.py` | Actions-side source requests, byte/hash verification, batch manifests | [source-ingestion.md](../docs/phase-2/source-ingestion.md), [github-acquisition.md](../docs/phase-2/github-acquisition.md) |
| `collector/upload.py` | Native-byte upload to Databricks staging via the verified Files API | [github-acquisition.md](../docs/phase-2/github-acquisition.md) |
| `contracts/` | Explicit `StructType`/`StructField` input contracts, one per source variant | [pipeline-behavior.md](../docs/phase-2/pipeline-behavior.md), [data-models.md](../docs/phase-2/data-models.md) |
| `transforms/staging_to_bronze.py` | Staging-to-Bronze unit with deterministic provenance MERGE | [staging-and-recovery.md](../docs/phase-2/staging-and-recovery.md) |
| `transforms/bronze_to_silver.py` | Bronze-to-Silver unit with conditional MERGE and quarantine | [pipeline-behavior.md](../docs/phase-2/pipeline-behavior.md) |

Rules the future implementation must satisfy (from the reviewed specification, not yet implemented):

- Explicit schema before every Spark read; no `inferSchema`, no inferred fixtures.
- Source-specific schemas are finalized only against acquired payloads; they are never invented.
- Runtime metadata never enters `record_hash`; a same-data Silver replay must change nothing.
- Raw payloads, secrets and unsanitized outputs stay out of Git.
