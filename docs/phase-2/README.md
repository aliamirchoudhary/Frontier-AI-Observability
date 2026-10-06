# Bronze and Silver implementation

Frontier AI Observatory will turn published evaluation and model metadata into traceable, validated lakehouse records using PySpark and Delta Lake on Databricks Free Edition.

**Status: implementation specification.** This documentation pack defines the intended behavior. Repository code, workspace execution and acceptance evidence must be checked before any feature is marked implemented.

| Document | Purpose |
| :--- | :--- |
| [Scope and acceptance](scope-and-acceptance.md) | Required behavior and evidence |
| [Source ingestion](source-ingestion.md) | Original payloads, acquisition and update semantics |
| [Data models](data-models.md) | Proposed grains, columns, keys and timestamps |
| [Pipeline behavior](pipeline-behavior.md) | Contracts, replay, backfills and quarantine |
| [Audit and recovery](audit-and-recovery.md) | Logging, write metrics and interrupted runs |
| [Environment and FinOps](environment-and-finops.md) | Serverless setup and resource controls |
| [Execution guide](execution-guide.md) | Parameter contract and planned execution examples |
| [Verification](verification.md) | Meaningful acceptance tests |
| [Submission evidence](submission-evidence.md) | Evidence to retain before release |

Repository: https://github.com/aliamirchoudhary/Frontier-AI-Observability

Gold tables, BI dashboards and empirical research results remain later work. Silver retains the distinctions needed for those analyses: evaluation protocol, model version, deployment alias, publication date and price observation time.
