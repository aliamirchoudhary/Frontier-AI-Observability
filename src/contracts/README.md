# src/contracts — PLANNED SCAFFOLD (Phase 2, Task 01)

**Status: planned. No schema is defined in this package yet.**

Rules from the reviewed specification ([pipeline-behavior.md](../../docs/phase-2/pipeline-behavior.md), [data-models.md](../../docs/phase-2/data-models.md)):

1. Every Spark input read — including nested JSON — is preceded by an explicit `StructType`/`StructField` definition. No `inferSchema`, no inferred `createDataFrame` fixtures.
2. Source-specific contracts are finalized against **acquired payloads** (Parquet footers inspected inside Databricks are discovery, not permission to infer at read time). Fields are never invented before the payload is inspected.
3. Contracts are versioned (`schema_version`); a physical source contract and the Bronze envelope contract are distinct.
4. Preflight compares physical fields/types to the registered contract before any Spark action; unknown fields quarantine rather than silently drop.
5. The common Bronze/Silver envelope columns are specified in [data-models.md § Common conventions](../../docs/phase-2/data-models.md); they will be transcribed here once their implementation task begins.

No `StructType` code is written in Task 01 because the source-specific payloads that define them have not been acquired under the Phase 2 route, and inventing field lists is prohibited.
