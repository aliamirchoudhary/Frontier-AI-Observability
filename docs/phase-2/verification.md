# Verification plan

Run cloud acceptance tests on isolated table names and fixed small fixtures, then execute the real baseline and native incremental batch once. Fixtures are test-only and must never be counted as acquired source data. Every Spark fixture has an explicit schema.

| Test | Procedure | Pass condition |
| :--- | :--- | :--- |
| Contract coverage | Compare every source variant and nested record with its registered contract | Explicit schema before every file read; unapproved fields/types detected |
| Baseline | Process the complete approved original source manifest | Original byte/hash inventory matches; all core sources produce useful Bronze/Silver records or explicitly investigated rejects |
| Exact replay | Capture Silver rows including timestamps, repeat identical batch, compare both directions | exceptAll comparison is empty both ways; key counts unchanged; logged inserts/updates zero |
| Real increment | Process native post-baseline Arena latest files | Original 1,219,849 bytes verified; chronology holds; analytical changes are traced, not assumed equal to 21,896 input rows |
| Correction | Change one permitted analytical value in an isolated fixture with newer authority | Exactly intended key updates; hash/load_timestamp changes; other records unchanged |
| Conflicting keys | Two different payloads with same business identity and no authoritative order | Conflict quarantined; no arbitrary winning row |
| Old backfill | Run historical batch after newer observations | History is retained; newer current state is not downgraded |
| Layer-only replay | Staging-to-Bronze then Bronze-to-Silver independently | No today-only dependency, duplicate provenance or Silver mutation on unchanged replay |
| Extra field | Add an unexpected field/header to a test source | Detected before projection; quarantined under the selected policy |
| Changed type | Supply unsafe number/string drift and a valid neighboring file | Invalid unit quarantined; valid unit completes; run reports partial quality accurately |
| Bad date / count | Invalid date, fractional or out-of-range whole count, nonfinite metric | Reason-coded quarantine or explicit allowed-null rule; no silent truncation |
| Corrupt file | Truncate an isolated Parquet fixture; force execution | File-level failure captured with original reference; other files proceed |
| Missing evaluation | Study result without evaluation member | Missing status retained; no invented success |
| PII | Inspect approved Silver fields and sampled restricted rejects | Contact/log payload fields absent from Silver and public evidence |
| Audit | Compare each unit with its attributable Delta history | Correct file, layer, times, status and actual inserted/updated metrics |
| Interrupted commit | Inject a test interruption after target write but before terminal audit | Recovery reconciles committed version and replay creates no duplicate data |
| Logging failure | Simulate unavailable log writer in isolated test | Further target writes stop; no false success |

Use a content comparison, not only row counts, for idempotency. Compare load_timestamp too. An expected fixture timestamp update must be evaluated after actions materialize; Spark expressions may otherwise be lazy. Evidence should identify Git commit, test inputs, runtime, parameters and actual results. Sanitized SQL results can be published; raw failures, credentials and personal identifiers cannot.

## Additional acceptance gates

- Every source payload call runs on Actions; unchanged uploads are verified in Databricks staging and all Spark execution is in Databricks. Instructor source-location approval remains pending.
- Metadata/native payload downloads and redirects are proven on Actions, with verified Databricks volume upload/readback. Transfer/authentication blockers remain BLOCKED.
- Staging original files/manifests and Bronze Delta record history are visibly distinct persistent stores.
- A partial staged file is never consumed; Source-to-Staging failure/no-op attempts are logged.
- Test-only F0 + multiple increment batches reconstruct missing Bronze without duplicate business observations or state downgrade.
- A recreated table uses a new recovery generation and does not skip replay based on stale old checkpoints.
- Silver exact-content replay remains unchanged even when rebuilt Bronze has new processing timestamps.
- Missing historical raw/table data is reported as irrecoverable where source retention/backups cannot restore it.
