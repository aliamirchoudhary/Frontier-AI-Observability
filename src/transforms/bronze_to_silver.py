"""PLANNED — Bronze-to-Silver unit. Not implemented.

Status: Task 01 scaffold only. This module reads no table and writes no table.

Specification (binding when implemented):
  docs/phase-2/pipeline-behavior.md — conditional MERGE equivalent to
      WHEN MATCHED AND target.record_hash <> source.record_hash
      AND source_is_authoritative_newer THEN UPDATE ...;
      unchanged matches do not update timestamps; runtime fields are excluded
      from record_hash; conflicts without source order quarantine instead of
      dropping duplicates
  docs/phase-2/data-models.md — Silver grains and keys, non-null business-key
      components, casting rules, reconstruction-timestamp rules
  docs/phase-2/verification.md — exact replay must be empty in both directions
      (exceptAll), with logged inserts/updates zero and timestamps preserved
  docs/phase-2/audit-and-recovery.md — audited units with actual
      insert/update metrics from attributable Delta operationMetrics

Entry points raise NotImplementedError until the Silver implementation task
runs inside Databricks Free Edition with witnessed evidence.
"""


def planned_only(*_args, **_kwargs):
    """Every Bronze-to-Silver entry point until it is implemented."""
    raise NotImplementedError(
        "PLANNED: Bronze-to-Silver is not implemented. "
        "See docs/phase-2/pipeline-behavior.md and docs/phase-2/verification.md."
    )
