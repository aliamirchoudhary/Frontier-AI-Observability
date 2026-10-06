# Environment and FinOps

Databricks Free Edition is the execution target. Keep local collection, contract inspection and small pure-Python tests lightweight; run Spark and Delta acceptance tests in the workspace.

## Setup decisions to verify

Record the observed catalog, writeable schemas, volume path, Python/Spark environment, module import route and available notebook/job parameter APIs. Confirm privileges before creating objects. Use actual identifiers, not assumed main/default catalog names. The original artifact location is a Unity Catalog volume; analytical tables use fully qualified managed Delta names.

Use an HTTPS Git folder when supported in the account. If Git integration is blocked, use a supported notebook/module import route, then commit/export the exact executed source and record its Git commit. Do not share account credentials between operators. Cross-account workspace collaboration is a capability to verify, not an assumption; an execution-owner workspace can be reviewed through sanitized evidence and Git.

## Free Edition constraints

Free Edition uses serverless compute, limits usage under a fair-use policy and restricts outbound network destinations. Exceeding usage can suspend compute until quota resets. The official limits do not establish a universal fixed storage entitlement or guaranteed notebook-hours budget. A successful sample/full run is needed to measure this project's fit.

Use Spark Connect-compatible DataFrame and SQL APIs. Avoid RDD APIs, DBFS mounts, classic-cluster configuration, Spark cache/persist APIs and dependency assumptions that fail on serverless. Use a batch workflow; continuous processing is unnecessary. Local source collection and volume upload are the fallback for blocked publisher access, with checksum verification.

## Resource controls

Start with representative samples in isolated tables. Upload/process one source group at a time. Keep native archives, extract only useful result/evaluation JSON members, and delete temporary extracts only after durable write verification. Original compressed source totals are not peak storage requirements: Bronze envelopes, Silver, staging and Delta versions add overhead.

Record elapsed time, raw bytes, derived table sizes where measurable, rows and retained temporary artifacts. Avoid repeated baseline rebuilds, large driver collect/toPandas calls and unnecessary full counts in production. Acceptance counts are bounded, deliberate verification. Keep one writer per target and run acceptance steps sequentially.

Do not install replacement Spark/Delta runtimes into the managed workspace. Verify available runtime libraries first; add only necessary supported notebook dependencies. Do not run model inference, benchmark Docker stacks, paid jobs or quota-evading account workarounds. Pause when quotas are exhausted; resume via the audited replay workflow.

## Official references

- https://docs.databricks.com/aws/en/getting-started/free-edition-limitations
- https://docs.databricks.com/aws/en/compute/serverless/limitations
- https://docs.databricks.com/aws/en/volumes/volume-files
- https://docs.databricks.com/aws/en/repos/limits
- https://docs.databricks.com/aws/en/tables/history
- https://docs.databricks.com/aws/en/tables/operations/custom-metadata
