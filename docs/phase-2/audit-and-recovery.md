# Audit and recovery

Operational schemas are explicit and separate from business tables. Store payload references in logs, not personal content or secrets.

## Operational dictionaries

| Table | Key | Columns and types |
| :--- | :--- | :--- |
| pipeline_runs | run_id | run_id STRING; batch_id STRING; retry_of_run_id STRING nullable; mode STRING; parameters_json STRING sanitized; started_at TIMESTAMP; ended_at TIMESTAMP nullable while running; status STRING; code_commit STRING nullable; schema_version STRING; error_code STRING nullable; error_summary STRING nullable; load_timestamp TIMESTAMP |
| pipeline_execution_logs | run_id + unit_id + attempt_number | run_id STRING; unit_id STRING; attempt_number INT; batch_id STRING; layer STRING; source_id STRING; parameter_or_file STRING; target_table STRING nullable; started_at TIMESTAMP; ended_at TIMESTAMP nullable while running; status STRING; rows_read BIGINT nullable; rows_valid BIGINT nullable; rows_inserted BIGINT nullable; rows_updated BIGINT nullable; rows_deleted BIGINT nullable; rows_quarantined BIGINT nullable; rows_unchanged BIGINT nullable; delta_version_before BIGINT nullable; delta_version_after BIGINT nullable; metrics_verified BOOLEAN; error_code STRING nullable; error_summary STRING nullable; load_timestamp TIMESTAMP |
| source_file_inventory | source_artifact_id | source_artifact_id STRING; source_id STRING; source_revision STRING nullable; source_url STRING; artifact_path STRING; original_bytes BIGINT; sha256 STRING; format STRING; source_observed_at TIMESTAMP; batch_id STRING; processing_status STRING; last_successful_run_id STRING nullable; schema_version STRING nullable; load_timestamp TIMESTAMP |
| quarantine_records | quarantine_id | quarantine_id STRING; run_id STRING; batch_id STRING; source_id STRING; source_artifact_id STRING; source_record_key STRING nullable; layer STRING; reason_code STRING; reason_summary STRING sanitized; restricted_payload_reference STRING; schema_version STRING; detected_at TIMESTAMP; load_timestamp TIMESTAMP |

Required identifiers and timestamps are non-null except where explicitly noted. Inventory update fields reflect successful reconciliation, not simply a received file. Quarantine identity is deterministic per artifact, record/reason and contract so retries do not flood the same rejection; attempts remain visible in logs. Use artifact-level references when parsing never produced rows.

## Audit semantics

Write an entry for every processed file or target-table unit, across Source-to-Staging, Staging-to-Bronze and Bronze-to-Silver, for full loads, increments, replays and backfills. Use statuses such as RUNNING, SUCCESS, NO_OP, QUARANTINED, PARTIAL and FAILURE with documented meanings. Final entries have an end time. A top-level success requires all required units to finish under the accepted quality policy. Quarantined required units cannot be hidden under SUCCESS.

Rows inserted/updated refer to actual target changes, not input rows, source payload counts or numOutputRows. Obtain Delta operationMetrics for the attributable write version. MERGE provides numTargetRowsInserted and numTargetRowsUpdated; append operations use their supported write metrics with a clearly separate meaning. Do not fabricate zero when metrics are unknown after an interrupted commit; leave nullable values and mark metrics_verified false until recovery.

On serverless, do not depend on the classic-compute SparkSession commit metadata configuration. Writer userMetadata is available for DataFrameWriter writes; MERGE correlation must use a runtime-supported method. The fallback is one writer per target, record target version before and after the operation, examine the intervening history, and reject ambiguous attribution. Never select history(1) and assume the most recent commit belongs to this run. Compaction can add unrelated operation types; identify the expected MERGE version.

## Recovery

1. Locate nonterminal runs and processing units.
2. Check the affected target's version history and recorded before-version.
3. Reconcile attributable committed metrics; mark ambiguous cases unresolved.
4. Retry idempotently only after resolving writer ownership and the input manifest.
5. Record the new attempt, retain the original failure and finalize source inventory markers only after reconciliation.

If the logging store is unavailable, stop new writes. Keep a sanitized recovery note through an approved durable route and reconcile it later. A swallowed logging exception must not let the batch appear successful. Demonstrate a failure before commit and a simulated interruption after commit in isolated acceptance tables.

## Staging durability and recovery checkpoints

Add explicit acquisition log fields: bytes_received BIGINT nullable, original_bytes BIGINT nullable, checksum STRING nullable, request_host STRING, final_host STRING nullable and acquisition_status STRING. Do not log signed queries or secrets. Layer-specific insert/update conventions must be documented.

Add artifact_processing_checkpoints with logical key (source_artifact_id, layer, target_table, contract_version, recovery_generation). Fields: source_artifact_id STRING, batch_id STRING, layer STRING, target_table STRING, contract_version STRING, recovery_generation STRING, status STRING, last_successful_run_id STRING nullable, target_version BIGINT nullable, completed_at TIMESTAMP nullable, load_timestamp TIMESTAMP. Document exact nullability and every implementation addition. Processing status is not a single shared flag across layers.

Persist a sanitized append-only per-attempt event file in the separate audit area when supported, plus ready staging manifests. A catch block cannot run after a hard process kill: durable started entries remain nonterminal, and the next invocation reconciles them. No layer can promise to log a terminal failure instantly if the process is dead or every audit store is unavailable. If table logging is unavailable but the tested file route works, record the event there and stop target writes; reconcile later. If both routes fail, stop and report the observability gap through available job output. File logs and tables are separate writes, not an atomic transaction.
