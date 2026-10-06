# Pipeline behavior

## Contract enforcement

Define every Spark input schema with StructType and StructField, including nested JSON schemas. Do not use inferred reads, inferred createDataFrame fixtures or inferSchema. Local Parquet footer inspection is contract discovery; it does not permit an inferred Spark reader.

Preflight every artifact before a Spark action. Compare physical fields and types to the registered contract; a projected schema can otherwise hide newly added columns. For JSON and CSV, inspect raw keys/header and retain corrupt-record information under a declared schema. Unknown fields are not silently dropped. Choose quarantine as the default; do not enable broad automatic schema evolution.

Use source-specific parsing. CSV text fields can be declared as strings in Bronze and checked with safe casts in Silver. Handle ANSI casting failures using supported safe conversion expressions and explicit reject conditions. A row that violates a required contract goes to quarantine with a sanitized reason; the rest of a compatible file proceeds. An incompatible or corrupt file is quarantined as a file unit; compatible neighboring files continue. Tests must force Spark execution because schema and read errors may be deferred.

## Determinism and MERGE

Bronze MERGE uses deterministic provenance identity and inserts missing rows only. Silver MERGE joins on validated business identity and changes rows only when business content differs and the correction is eligible. Runtime fields are not part of record_hash.

For a correction table, the intended condition is equivalent to `WHEN MATCHED AND target.record_hash <> source.record_hash AND source_is_authoritative_newer THEN UPDATE ...`. Use explicit column mappings; unchanged matches do not update timestamps. New keys insert. Versioned catalog histories insert distinct content versions rather than overwriting history.

Validate uniqueness before MERGE. Identical duplicates can collapse deterministically; conflicting duplicates without a reliable source order are quarantined, not resolved using dropDuplicates, unordered first/last, random IDs or processing timestamps. Verify actual source-key uniqueness before approving proposed grains.

Historical backfills cannot downgrade a current-state table. Source revision hashes are not chronological counters. Use verified publisher chronology or explicit accepted snapshot ordering and distinguish publication time from observation time.

## Parameters and boundaries

Support mode, layers, sources, batch_id, artifact manifest/path, optional publication window, explicit catalog/schema/volume identifiers and dry_run. Do not bake today's date or a guessed main.default catalog into functions. Separate acquisition time, publication filter and execution time.

Date intervals are start-inclusive and end-exclusive. Sources without a compatible publication date use an explicit batch/artifact selection rather than a misleading date filter. An exact batch replay retains original source_observed_at; each attempt gets a fresh run_id.

Processing plans list exact files and tables, not broad recursive globs over everything in storage. Every action validates that the path is inside the configured source boundary. A dry run validates the plan and available contracts without writing analytical tables; it may record an operational dry-run event if documented.

## Failures and resumption

Use bounded retries for transient acquisition errors and retain failed-attempt logs. Never advance a successful-processing marker before validation, writes and audit reconciliation complete. Source downloads and Delta writes are separate checkpoints.

A committed table write and an audit write are not an atomic multi-table transaction. Interrupted runs must be detected and reconciled with attributable Delta versions; logs must not claim a write was rolled back if it committed. Serialize writers per target table, require explicit retry/recovery and reuse idempotent table logic. A retry creates a new attempt and links to the prior run.

No file deletion, table overwrite, zero-retention VACUUM or unbounded scheduled compute is part of the default workflow.
