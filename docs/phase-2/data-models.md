# Bronze and Silver data models

These are target contracts. Source-specific nested schemas must be finalized against acquired payloads before implementation. The implementation must document every additional column; generic dictionaries are not a substitute for source StructType definitions.

## Common conventions

Logical keys are enforced by validation and MERGE; do not assume Spark primary-key declarations enforce uniqueness. Use canonical JSON/struct serialization for keys and content hashes, with explicit null handling, stable map ordering and preserved array meaning. Do not concatenate ambiguous strings.

Every Bronze and Silver record includes the following columns. Carry original source ingestion time forward separately from processing time.

| Column | Spark type | Null? | Meaning |
| :--- | :--- | :---: | :--- |
| record_id | StringType | No | Deterministic row identity in its table |
| source_id | StringType | No | Reviewed source registry identifier |
| source_record_key | StringType | No | Canonical source-level business identity |
| source_artifact_id | StringType | No | Source file checksum plus source/format namespace |
| source_revision | StringType | Yes | Publisher immutable revision when available |
| source_publication_date | DateType | Yes | Published observation date, not download date |
| source_observed_at | TimestampType | No | UTC acquisition time of the source response |
| batch_id | StringType | No | Accepted batch that introduced or corrected this row |
| record_hash | StringType | No | SHA-256 of analytical/source payload, excluding runtime metadata |
| load_timestamp | TimestampType | No | UTC first insert or latest meaningful change in this layer |
| source_load_timestamp | TimestampType | Yes | Bronze processing time carried to Silver; null only in Bronze |

A no-op replay does not change record_id, hash, batch_id or timestamps in Silver. Append-only Bronze provenance records retain their first load time. Operations logs record every attempt separately.

## Bronze

Original artifacts remain unchanged in the volume. The proposed Delta `bronze_source_records` table is a provenance envelope around each contracted source record, not a replacement for the original files.

| Additional column | Type | Null? | Meaning |
| :--- | :--- | :---: | :--- |
| entity_type | StringType | No | arena_observation, model, benchmark, price, release, study_result or study_evaluation |
| source_relative_path | StringType | No | Safe artifact path, or archive/member path |
| source_row_locator | StringType | No | Stable source key plus occurrence handling; no generated Spark row ID |
| schema_version | StringType | No | Explicit source contract version |
| payload_json | StringType | No | Source record values represented losslessly within the documented logical contract |

Bronze logical key: source_artifact_id + entity_type + source_row_locator. record_id is the hash of that canonical key. A new source revision can add new provenance records even when Silver business content is unchanged. Replaying the same artifact cannot duplicate Bronze rows.

Physical source contracts and envelope contracts are distinct. Parquet retains native numeric types in its source reader before values are placed in the envelope. JSON envelope serialization is not used to inflate measured acquisition size. If serialization cannot preserve a field, fix the contract or quarantine; do not silently discard it.

Source records with known safe types enter Bronze; incompatible files remain preserved as artifacts and referenced in quarantine. Every landed file has an operational inventory record, even if no Bronze record can be parsed.

## Silver

Each table uses the common columns plus the listed analytical columns. Additional source fields require reviewed dictionary entries. All business-key components are non-null; missing key components are quarantined.

| Table | Grain and logical key | Analytical columns and target types |
| :--- | :--- | :--- |
| silver_arena_observations | source + subset/protocol + category + source model name + publication date; validate uniqueness on complete baseline | subset STRING, protocol STRING, category STRING, source_model_name STRING, source_organization STRING nullable, model_license STRING nullable, metric_name STRING, metric_value DOUBLE nullable, ci_lower DOUBLE nullable, ci_upper DOUBLE nullable, variance DOUBLE nullable, vote_count BIGINT nullable, observation_count BIGINT nullable, session_count BIGINT nullable, published_rank BIGINT nullable |
| silver_model_metadata | source model identity + distinct analytical content version | source_model_id STRING, model_name STRING, organization_name STRING nullable, release_date DATE nullable, metadata_json STRING containing only approved analytical fields |
| silver_benchmark_definitions | source benchmark identity + definition content version | source_benchmark_id STRING, benchmark_name STRING, metric_name STRING nullable, unit STRING nullable, direction STRING nullable, protocol STRING nullable, definition_json STRING with approved fields |
| silver_price_observations | source tariff identity/configuration + distinct content version | source_model_id STRING, provider STRING nullable, deployment_mode STRING nullable, currency STRING, input_price_per_million DECIMAL(20,8) nullable, output_price_per_million DECIMAL(20,8) nullable, cached_input_price_per_million DECIMAL(20,8) nullable, context_tier STRING nullable, effective_date DATE nullable, price_measured BOOLEAN |
| silver_model_releases | source model identity + distinct release metadata version | source_model_id STRING, model_name STRING, organization_name STRING nullable, release_date DATE nullable, release_precision STRING nullable, release_metadata_json STRING containing approved fields |
| silver_study_results | study + setting + repository + task + feature pair + publisher run ID | study_id STRING, setting STRING, repository_name STRING, task_id BIGINT, feature_ids ARRAY<BIGINT>, publisher_run_id STRING, source_model_alias STRING, harness STRING nullable, started_at TIMESTAMP nullable, ended_at TIMESTAMP nullable, duration_seconds DOUBLE nullable, cost_measured BOOLEAN, reported_cost DECIMAL(20,8) nullable |
| silver_study_evaluations | same study/run/task identity plus evaluation identity or content version where publisher provides it | study_id STRING, setting STRING, repository_name STRING, task_id BIGINT, feature_ids ARRAY<BIGINT>, publisher_run_id STRING, evaluation_present BOOLEAN, both_features_passed BOOLEAN nullable, merge_failed BOOLEAN nullable, outcome_json STRING containing approved outcome fields |
| silver_model_mappings | source + source model identity + reviewed mapping version | source_model_id STRING, canonical_model_id STRING nullable, canonical_organization_id STRING nullable, match_status STRING, evidence_reference STRING nullable |

SQL types above map to explicit PySpark types: STRING to StringType, BIGINT to LongType, DOUBLE to DoubleType, TIMESTAMP to TimestampType, DATE to DateType, BOOLEAN to BooleanType, DECIMAL to DecimalType, ARRAY to ArrayType. Decimal scale and input price units must be checked against source precision before approval.

History record_id includes the logical entity key and content hash for versioned catalog observations. For Arena and run outcomes, corrections update the same established observation key when a demonstrably newer source authority corrects it. Price/source histories retain earlier versions. source_observed_at identifies first observation of that version. Returning to a previously seen value needs an explicit observation/event policy if chronological transitions must be retained; do not silently claim continuous price history from deduplicated versions.

Optional current-state tables are separate from these histories. If created, document every column, include load_timestamp, and prevent older backfills from replacing newer accepted state. Reviewed mappings may remain unresolved; retain useful source records rather than forcing a match.

## Specific casting rules

Inspected samples show text rank and vote_count as DOUBLE; style-controlled text rank BIGINT and vote_count DOUBLE; webdev rank and vote_count BIGINT. Agent observation/session counts are DOUBLE. Recheck full and incremental physical schemas separately. A Parquet DOUBLE cannot safely be read with a forced BIGINT schema merely because values look integral.

Read each physical contract correctly, then check finiteness, whole-number values and range before conversion to LongType. Keep agent score separate from Arena rating; no nonnegative constraint on a score whose protocol permits negative values. Validate interval ordering and metrics within source-specific units. Dates without a documented timezone are not silently labeled UTC; preserve raw values and resolve the source convention, or retain null analytical timestamps with a documented reason where permitted.

Missing study evaluations remain missing. Do not infer success from a Submitted agent status or reconstruct unavailable evaluation files. Zero-filled study cost and token values become null/unmeasured in Silver while originals remain available in restricted Bronze.
