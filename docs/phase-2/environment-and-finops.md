# Environment and FinOps

## Runtime locations

PC: Git, editor and coding agent. Optional GitHub CLI supports separately authorized GitHub operations. No mandatory local venv, Python, Java or Spark. Full datasets are not stored on the PC.

Actions: standard hosted runner, reviewed Python acquisition dependencies, bounded temporary files, original-payload collection and upload. Check actual repository runner/storage allowances and account settings before enabling schedules. No paid runner or storage upgrade.

Databricks Free Edition: notebook environment, Spark DataFrame/SQL transformations, Unity Catalog staging volume, separate managed Bronze/Silver Delta histories, audit tables and acceptance queries. Verify actual catalog/schema/volume names and privileges. Free Edition has fair-use compute quotas and restricted egress; no guaranteed fixed storage or notebook-hour entitlement is assumed.

## Resource controls

Prove tiny transfer first; run representative cloud samples before full source groups. Sequential jobs and one writer per target. Keep immutable source archives; extract only required safe result/evaluation members and clean disposable extracts after successful durable processing. Do not execute archive code.

Reference compressed baseline is 216.37 MB plus supplements. Decoded CooperBench contents exceed 1 GB, so compressed bytes are not peak storage. The existing 3 GB working estimate is a planning target to measure and revise, not an entitlement or a guaranteed sufficient cap. Stage, Bronze, Silver, retained Delta versions and temporary extracts all count.

Track runner elapsed time, transfer bytes, cloud execution time, table sizes where measurable and retained files. No repeated baseline collection on code pushes. No large driver collect/toPandas calls or continuous Spark streaming. Stop at exhausted quotas; resume audited units. Artifacts and Actions logs have retention and must not be used as the only recovery history.

## Cloud setup

Verify supported Git folder or notebook/module import route, fresh-session imports and executed source SHA. Shared workspace access is an observed capability; otherwise one execution owner runs cells and shares sanitized evidence for the other reviewer. Never share passwords or personal tokens. Managed Spark/Delta are not replaced through pip. Use supported minimal notebook dependencies with an explicit environment manifest.

Use Spark Connect-compatible DataFrame/SQL APIs; no RDDs, DBFS mounts or unsupported cache/config APIs. All Spark tests run in Databricks. Runner tests validate acquisition code only and cannot establish cloud ingestion success.

## References

- https://docs.databricks.com/aws/en/getting-started/free-edition-limitations
- https://docs.databricks.com/aws/en/compute/serverless/limitations
- https://docs.databricks.com/api/files/v2/file
- https://docs.github.com/en/actions/how-tos/manage-workflow-runs/remove-workflow-artifacts
