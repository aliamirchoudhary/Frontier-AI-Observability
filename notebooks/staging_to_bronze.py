# Databricks
# PLANNED SCAFFOLD — Staging to Bronze thin notebook (Phase 2, Task 01).
# Status: NOT IMPLEMENTED and NEVER EXECUTED. No cloud run has occurred; this
# file must not be presented as a working pipeline entry point.
#
# Design: thin notebook only — parameter capture and delegation. All logic is
# planned for src/transforms/staging_to_bronze.py (also a PLANNED scaffold).
# Parameter contract mirrors docs/phase-2/execution-guide.md exactly.

# Databricks-only name; never imported or run outside a Databricks session.
dbutils.widgets.text("mode", "incremental", "mode")
dbutils.widgets.text("layers", "staging_to_bronze", "layers")
dbutils.widgets.text("sources", "", "sources")
dbutils.widgets.text("batch_id", "", "batch_id")
dbutils.widgets.text("manifest_path", "", "manifest_path")
dbutils.widgets.text("input_path", "", "input_path")
dbutils.widgets.text("start_date", "", "start_date")
dbutils.widgets.text("end_date", "", "end_date")
dbutils.widgets.text("catalog", "", "catalog")
dbutils.widgets.text("bronze_schema", "", "bronze_schema")
dbutils.widgets.text("silver_schema", "", "silver_schema")
dbutils.widgets.text("ops_schema", "", "ops_schema")
dbutils.widgets.text("volume_root", "", "volume_root")
dbutils.widgets.text("dry_run", "true", "dry_run")

PARAMETERS = {
    name: dbutils.widgets.get(name)
    for name in (
        "mode", "layers", "sources", "batch_id", "manifest_path", "input_path",
        "start_date", "end_date", "catalog", "bronze_schema", "silver_schema",
        "ops_schema", "volume_root", "dry_run",
    )
}

# Planned sequence (docs/phase-2/execution-guide.md): verify staging manifest,
# dry-run plan, then execute and inspect audit rows. None of it is built.
raise NotImplementedError(
    "PLANNED: Staging-to-Bronze is not implemented. "
    "See docs/phase-2/execution-guide.md and docs/phase-2/staging-and-recovery.md."
)
