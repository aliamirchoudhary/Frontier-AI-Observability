# Execution guide

**Status: parameter specification, not an executable entry point yet.** The implementation must replace this page's illustrative invocation with its actual tested notebook/function commands and parameter names.

## Prerequisites

A reviewed source manifest, explicit schemas, a writeable Databricks Free Edition catalog/schema, a verified volume upload, deployed code matching a Git commit, and initialized operational tables are required. Use an isolated acceptance namespace before production-like tables.

| Parameter | Meaning |
| :--- | :--- |
| mode | full, incremental or backfill; controls planning, not unsafe overwrites |
| layers | raw_to_bronze, bronze_to_silver or both |
| sources | Explicit reviewed source identifiers |
| batch_id | Stable identifier for the selected artifact batch |
| manifest_path | Absolute approved volume manifest or documented input route |
| input_path | Optional bounded artifact selection; must agree with manifest |
| start_date / end_date | Optional publication interval, inclusive start/exclusive end |
| catalog / bronze_schema / silver_schema / ops_schema | Actual approved Unity Catalog identifiers |
| volume_root | Actual /Volumes/catalog/schema/volume prefix |
| dry_run | Validate and print a sanitized plan before analytical writes |

Illustrative parameter object:

```json
{
  "mode": "incremental",
  "layers": "both",
  "sources": ["arena"],
  "batch_id": "arena-native-increment-01",
  "manifest_path": "<actual-volume-root>/manifests/arena-native-increment-01.json",
  "dry_run": true
}
```

Values in angle brackets must be supplied from observed setup. This is not a CLI command. The same batch_id and source observations must be retained for exact replay; run_id is generated per attempt.

## Standard sequence

1. Acquire or select a manifest. Verify bytes and source hashes.
2. Run a dry plan and inspect files, source contracts, dates and target names.
3. Execute the baseline in both layers, then inspect quality and audit results.
4. Execute the subsequent native incremental batch in both layers.
5. Replay that exact increment and confirm zero Silver inserts/updates and unchanged timestamps.

## Historical backfill

Select a previously acquired batch/path and an optional compatible publication interval. Execute raw_to_bronze to reconstruct missing Bronze records. Then execute bronze_to_silver independently using its batch/artifact selector. Both operations must be repeatable without duplication. Do not redownload current data and call it a historical backfill.

Inspect audit rows, rejected units, target changes and accepted source ordering after each stage. Older content cannot replace a newer current-state observation. A date filter does not apply to a source without documented publication dates; select that source by batch instead.

## Recovery and scheduling

Use the recovery procedure for interrupted writes before retrying. Scheduling is optional until the exact manual path succeeds. If available, configure one bounded job with required parameters, a sensible timeout and serialized target writes. Network blocks require the validated local collector/upload route; do not claim automatic collection until that handoff is tested.
