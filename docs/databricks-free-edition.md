# Databricks Free Edition plan

Official limits: https://docs.databricks.com/aws/en/getting-started/free-edition-limitations

## What the project uses

- PySpark and Delta on serverless notebook compute.
- A single SQL warehouse and dashboard over Gold tables.
- Sequential or bounded scheduled tasks; the plan does not require more than five concurrent job tasks.
- Existing public source data; no paid inference or GPU is needed.

## Verified platform constraints

Free Edition permits only serverless compute and limits notebook compute size and usage. It allows one SQL warehouse up to 2X-Small and a maximum of five concurrent job tasks per account. Outbound internet access is restricted to trusted domains. Free Edition is for noncommercial use and has no guaranteed SLA. If fair-use quotas are exceeded, compute can stop for the rest of the day or, in extreme cases, the month; data and settings are retained.

The official limits page does not give a universal numeric storage allowance or fixed notebook-hours budget. The **3 GB working-storage target is an internal estimate**, not a claimed Databricks entitlement. Availability and quota behavior must be confirmed in the actual workspace.

## Resource estimate and safeguards

Original core downloads total 216.37 MB. Supplemental catalogs bring initial acquisition to approximately 227 MB. The original CooperBench archives are 106.37 MB compressed and approximately 1,044 MB after extraction. Allow room for Parquet decoding, Delta tables, quarantined records and temporary files; actual peak usage must be measured.

Begin with small public samples. Ingest one study setting at a time, extract only relevant members for processing, and remove temporary extracts after successful ingestion. Avoid keeping repeated full copies in memory. Retain original archives for reproducibility. Process available changes weekly, skip unchanged files, and avoid repeatedly rebuilding the entire baseline.

Test source connectivity before enabling collection. If outbound restrictions block the publisher, use a local collector and a supported authenticated workspace upload route. Validate that route and scheduling with a sample batch before relying on it. This upload integration is planned, not implemented by this package.

Run the sample workflow, then the full baseline once; record runtime and storage. Pause optional refreshes if quotas are reached. Do not enable paid billing resources. A future commercial service will need infrastructure and data rights that permit commercial use.

## Readiness

The data scale is reasonable for a Free Edition trial of this design. This package has not executed the full cloud pipeline or established its compute-quota consumption. A successful workspace trial is required before claiming the complete workflow fits the account's quota.
