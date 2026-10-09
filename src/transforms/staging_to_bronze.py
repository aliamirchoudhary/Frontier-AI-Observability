"""PLANNED — Staging-to-Bronze unit. Not implemented.

Status: Task 01 scaffold only. This module reads no files and writes no table.

Specification (binding when implemented):
  docs/phase-2/staging-and-recovery.md — staging (immutable native files) and
      Bronze (managed Delta provenance history) are separate stores
  docs/phase-2/data-models.md — Bronze logical key:
      source_artifact_id + entity_type + source_row_locator; record_id is the
      hash of that canonical key; every record carries load_timestamp
  docs/phase-2/pipeline-behavior.md — deterministic provenance MERGE that
      inserts missing rows only; replaying the same artifact never duplicates
      Bronze rows and never rewrites existing timestamps
  docs/phase-2/audit-and-recovery.md — one audited unit per artifact/target,
      with attributable Delta version metrics

Entry points raise NotImplementedError until the Bronze implementation task
runs inside Databricks Free Edition with witnessed evidence.
"""


def planned_only(*_args, **_kwargs):
    """Every staging-to-Bronze entry point until it is implemented."""
    raise NotImplementedError(
        "PLANNED: Staging-to-Bronze is not implemented. "
        "See docs/phase-2/staging-and-recovery.md and docs/phase-2/data-models.md."
    )
