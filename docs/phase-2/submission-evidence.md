# Submission evidence

This checklist remains open until each item has linked execution evidence. Do not mark a test passed because its code exists.

- [ ] PySpark modules and notebooks are committed and execute in Databricks Free Edition.
- [ ] README links to complete actual Bronze and Silver dictionaries, including column names, types, nullability and logical keys.
- [ ] Every file reader has an explicit StructType/StructField contract; no inferred Spark reads or inferred test fixtures.
- [ ] Every Bronze/Silver record has a non-null load_timestamp.
- [ ] Conditional MERGE INTO behavior is demonstrated with identical replay and an eligible correction.
- [ ] Backfills work for Raw-to-Bronze and Bronze-to-Silver independently.
- [ ] Unexpected fields, unsafe type changes and corrupt files are isolated and audited.
- [ ] Separate operational tables record every full/incremental processing unit across both layers.
- [ ] Logs contain layer, parameter/file, start/end, status and actual rows inserted/updated.
- [ ] Full original baseline inventory and native incremental bytes are verified without format expansion or duplicate padding.
- [ ] CooperBench contributes task/outcome tables; evaluation coverage and unknown costs are disclosed.
- [ ] Private payloads, credentials, full raw datasets and private agent instructions are absent from Git history and submission files.
- [ ] Execution guide contains tested commands/parameters for standard incremental loads and historical backfills.
- [ ] Exact executed code commit and sanitized acceptance evidence are retained.
- [ ] A second operator has reviewed the evidence and followed the execution guide.

Suggested evidence location: docs/phase-2/evidence/. Add actual sanitized reports only after execution. Do not add placeholder passed reports or fabricated cloud screenshots.

Repository: https://github.com/aliamirchoudhary/Frontier-AI-Observability
