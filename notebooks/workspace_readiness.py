# Databricks
# Task 02 — workspace readiness notebook (thin; synthetic data only; NEVER a source pipeline).
# Run in a FRESH session after attaching this repository (Git folder or uploaded files).
# Nothing here touches real source payloads, Gold, dashboards or billing resources.
#
# Required widgets have EMPTY defaults on purpose: this notebook must never invent
# main/default catalog paths. Supply the approved identifiers from your workspace review.
# synthetic_id / expected_sha256 ship with the documented Task 02 synthetic constants
# (51-byte payload; hash computed and recorded in the repo, not a guess).
#
# Verifies: (1) staged synthetic readback hash, (2) explicit-schema fixture + conditional
# MERGE + Delta history on an ISOLATED task02_ managed table with load_timestamp
# preservation, (3) supported module import route, (4) runtime and code-SHA recording.
# See docs/phase-2/implementation-evidence/task-02-checklist.md for exact human steps.

dbutils.widgets.text("catalog", "", "catalog")
dbutils.widgets.text("bronze_schema", "", "bronze_schema")
dbutils.widgets.text("ops_schema", "", "ops_schema")
dbutils.widgets.text("volume_root", "", "volume_root")
dbutils.widgets.text("synthetic_id", "task-02-smoke-01", "synthetic_id")
dbutils.widgets.text("expected_sha256", "a684c4422a38df806f861c6ae4fa589ca847e4ffdbe2b69109f10ae2dfcd06f8", "expected_sha256")
dbutils.widgets.text("code_sha", "", "code_sha = git rev-parse HEAD")
dbutils.widgets.text("repo_path", "", "repo_path = optional import root")

# ---------------------------------------------------------------------------
# CELL 1 — parameters and bounded validation (fail fast, no invented defaults)
# ---------------------------------------------------------------------------
params = {name: dbutils.widgets.get(name).strip() for name in (
    "catalog", "bronze_schema", "ops_schema", "volume_root",
    "synthetic_id", "expected_sha256", "code_sha", "repo_path",
)}
catalog = params["catalog"]
bronze_schema = params["bronze_schema"]
ops_schema = params["ops_schema"]
volume_root = params["volume_root"].rstrip("/")
synthetic_id = params["synthetic_id"]
expected_sha256 = params["expected_sha256"]
code_sha = params["code_sha"]
repo_path = params["repo_path"]

missing = [k for k in ("catalog", "bronze_schema", "ops_schema", "volume_root") if not params[k]]
if missing:
    raise ValueError(f"Refusing to run with invented paths; supply approved values for: {missing}")
if not volume_root.startswith("/Volumes/"):
    raise ValueError("volume_root must be an approved /Volumes/... path (not a DBFS path)")
if not all(c.isalnum() or c == "-" for c in synthetic_id) or not synthetic_id:
    raise ValueError("synthetic_id must contain only alphanumerics and dashes")
import re as _re
if not _re.fullmatch(r"[0-9a-f]{64}", expected_sha256):
    raise ValueError("expected_sha256 must be a lowercase 64-char hex digest")

target_table = f"`{catalog}`.`{bronze_schema}`.task02_smoke_fixture"
artifact_path = f"{volume_root}/smoke/task-02/{synthetic_id}/artifacts/synthetic.txt"

print(f"validated params: catalog={catalog} bronze_schema={bronze_schema} "
      f"ops_schema={ops_schema} synthetic_id={synthetic_id} "
      f"volume_root_length={len(volume_root)} code_sha={code_sha or 'MISSING'}")

# ---------------------------------------------------------------------------
# CELL 2 — record actual runtime and code state (never claim an unrecorded SHA)
# ---------------------------------------------------------------------------
import json, datetime

runtime = {
    "spark_version": spark.version,
    "dbr_label": None,
    "app_id": None,
    "recorded_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "code_sha": code_sha or None,
}
try:
    runtime["dbr_label"] = spark.conf.get("spark.databricks.clusterUsageTags.sparkVersion")
except Exception:
    runtime["dbr_label"] = None  # serverless may not expose this tag; record null, not a guess
try:
    runtime["app_id"] = spark.conf.get("spark.app.id")
except Exception:
    runtime["app_id"] = None
if not code_sha:
    print("WARNING: code_sha widget empty — evidence cannot be bound to a commit; "
          "rerun with code_sha=<git rev-parse HEAD> after the human pushes the branch.")
print("RUNTIME:", json.dumps(runtime))

# ---------------------------------------------------------------------------
# CELL 3 — independent Databricks-side readback of the staged synthetic artifact
# ---------------------------------------------------------------------------
import hashlib

with open(artifact_path, "rb") as fh:
    staged_bytes = fh.read()
staged_sha = hashlib.sha256(staged_bytes).hexdigest()
readback = {"path_unit": f"smoke/task-02/{synthetic_id}", "bytes": len(staged_bytes),
            "sha256": staged_sha, "expected_sha256": expected_sha256,
            "match": staged_sha == expected_sha256}
print("STAGED_READBACK:", json.dumps(readback))
if not readback["match"]:
    raise AssertionError(
        f"Staged synthetic artifact mismatch: got {staged_sha} ({len(staged_bytes)} bytes), "
        f"expected {expected_sha256} (51 bytes). Dispatch the Actions smoke workflow first "
        f"or fix the synthetic_id; do not continue."
    )

# ---------------------------------------------------------------------------
# CELL 4 — explicit-schema three-row fixture (no inference anywhere)
# ---------------------------------------------------------------------------
from pyspark.sql.types import StructType, StructField, StringType, LongType, TimestampType

fixture_schema = StructType([
    StructField("entity_id", StringType(), False),
    StructField("metric_name", StringType(), False),
    StructField("metric_value", LongType(), True),
    StructField("code_sha", StringType(), True),
    StructField("load_timestamp", TimestampType(), False),
])
fixed_ts = datetime.datetime(2026, 10, 9, 0, 0, 0, tzinfo=datetime.timezone.utc)
fixture_rows = [
    ("t02-1", "fixture_metric", 1, code_sha or None, fixed_ts),
    ("t02-2", "fixture_metric", 2, code_sha or None, fixed_ts),
    ("t02-3", "fixture_metric", 3, code_sha or None, fixed_ts),
]
source_df = spark.createDataFrame(fixture_rows, schema=fixture_schema)
print(f"FIXTURE: count={source_df.count()} schema={source_df.schema.simpleString()}")
assert source_df.count() == 3

# ---------------------------------------------------------------------------
# CELL 5 — isolated managed Delta target + conditional MERGE + history + replay
# ---------------------------------------------------------------------------
from delta.tables import DeltaTable

if not spark.catalog.tableExists(target_table):
    # DataFrameWriter.mode("errorifexists") is unmapped on Spark Connect runtimes
    # (UNSUPPORTED_OPERATION); plain CREATE TABLE (no IF NOT EXISTS) has identical
    # fail-if-exists semantics and runs on both classic and Connect.
    spark.sql(
        f"CREATE TABLE {target_table} ("
        "entity_id STRING NOT NULL, metric_name STRING NOT NULL, metric_value BIGINT, "
        "code_sha STRING, load_timestamp TIMESTAMP NOT NULL"
        ") USING DELTA"
    )
    print(f"created empty managed Delta target: {target_table}")

target = DeltaTable.forName(spark, target_table).alias("t")
history_before = target.history(1)
version_before = history_before.select("version").collect()[0][0]

# Conditional MERGE: insert new keys; update only when business content differs.
# load_timestamp is intentionally NOT in the update set so unchanged rows keep it.
(target.merge(
    source_df.alias("s"),
    "t.entity_id = s.entity_id",
)
.whenMatchedUpdate(condition="t.metric_value IS DISTINCT FROM s.metric_value OR t.metric_name IS DISTINCT FROM s.metric_name",
                   set={"metric_name": "s.metric_name", "metric_value": "s.metric_value", "code_sha": "s.code_sha"})
.whenNotMatchedInsert(values={"entity_id": "s.entity_id", "metric_name": "s.metric_name",
                              "metric_value": "s.metric_value", "code_sha": "s.code_sha",
                              "load_timestamp": "s.load_timestamp"})
.execute())

history_after = target.history(2)
metrics = history_after.select("version", "operation", "timestamp").collect()
op_metrics = history_after.select(
    "version", "operation",
    "operationMetrics.numTargetRowsInserted",
    "operationMetrics.numTargetRowsUpdated",
).collect()
# history(2) is newest-first; select this run's first-merge row by version, not by index.
first_merge_version = version_before + 1
first_merge_metrics = [r for r in op_metrics if r["version"] == first_merge_version]
if len(first_merge_metrics) != 1:
    raise AssertionError(
        f"expected exactly one first-merge version {first_merge_version} in history(2); "
        f"got versions {[int(r['version']) for r in op_metrics]}"
    )
print("MERGE_HISTORY:", json.dumps([
    {"version": r["version"], "operation": r["operation"]} for r in metrics
]))
print("MERGE_METRICS:", json.dumps([
    {"version": r["version"], "operation": r["operation"],
     "inserted": r["numTargetRowsInserted"], "updated": r["numTargetRowsUpdated"]}
    for r in op_metrics
]))

state_rows = spark.table(target_table).select(
    "entity_id", "metric_value", "load_timestamp").orderBy("entity_id").collect()
print("AFTER_FIRST_MERGE:", json.dumps([
    {"entity_id": r["entity_id"], "metric_value": r["metric_value"],
     "load_timestamp": r["load_timestamp"].isoformat()} for r in state_rows
]))

# Replay the EXACT same three rows: must insert 0 and update 0; timestamps preserved.
replay_before = {r["entity_id"]: r["load_timestamp"] for r in
                 spark.table(target_table).select("entity_id", "load_timestamp").collect()}
(target.merge(source_df.alias("s"), "t.entity_id = s.entity_id")
 .whenMatchedUpdate(condition="t.metric_value IS DISTINCT FROM s.metric_value OR t.metric_name IS DISTINCT FROM s.metric_name",
                    set={"metric_name": "s.metric_name", "metric_value": "s.metric_value", "code_sha": "s.code_sha"})
 .whenNotMatchedInsert(values={"entity_id": "s.entity_id", "metric_name": "s.metric_name",
                               "metric_value": "s.metric_value", "code_sha": "s.code_sha",
                               "load_timestamp": "s.load_timestamp"})
 .execute())
replay_metrics = target.history(1).select(
    "version", "operation",
    "operationMetrics.numTargetRowsInserted",
    "operationMetrics.numTargetRowsUpdated",
).collect()[0]
replay_after = {r["entity_id"]: r["load_timestamp"] for r in
                spark.table(target_table).select("entity_id", "load_timestamp").collect()}
replay = {
    "inserted": int(replay_metrics["numTargetRowsInserted"] or 0),
    "updated": int(replay_metrics["numTargetRowsUpdated"] or 0),
    "timestamps_preserved": replay_before == replay_after,
    "row_count": spark.table(target_table).count(),
}
print("EXACT_REPLAY:", json.dumps(replay))
assert replay["inserted"] == 0 and replay["updated"] == 0, "same-data replay must change zero rows"
assert replay["timestamps_preserved"], "load_timestamp changed on unchanged rows"

# ---------------------------------------------------------------------------
# CELL 6 — fresh-session module import route (record what works; never fake it)
# ---------------------------------------------------------------------------
import importlib, sys

import_result = {"route": None, "module": None, "error": None}
if repo_path:
    if repo_path not in sys.path:
        sys.path.append(repo_path)
    for candidate in ("src.transforms.bronze_to_silver", "transforms.bronze_to_silver",
                      "src.collector.acquire", "collector.acquire"):
        try:
            module = importlib.import_module(candidate)
            import_result = {"route": repo_path, "module": candidate,
                             "planned_marker": "NotImplementedError" in open(module.__file__).read()}
            break
        except Exception as exc:
            import_result["error"] = f"{candidate}: {type(exc).__name__}"
else:
    import_result["error"] = "repo_path widget empty; attach route not provided"
print("MODULE_IMPORT:", json.dumps(import_result))

# ---------------------------------------------------------------------------
# CELL 7 — sanitized readiness summary (no secrets, no tokens, no hostnames)
# ---------------------------------------------------------------------------
summary = {
    "task": "task-02",
    "runtime": runtime,
    "staged_readback_match": readback["match"],
    "fixture_rows": 3,
    "target_table_isolated": target_table.startswith(f"`{catalog}`.`{bronze_schema}`.task02_"),
    "merge_first_inserted": int(first_merge_metrics[0]["numTargetRowsInserted"] or 0),
    "merge_first_updated": int(first_merge_metrics[0]["numTargetRowsUpdated"] or 0),
    "exact_replay_zero_change": replay["inserted"] == 0 and replay["updated"] == 0,
    "timestamps_preserved": replay["timestamps_preserved"],
    "module_import_route_found": import_result["route"] is not None,
    "code_sha_recorded": bool(code_sha),
}
print("READINESS_SUMMARY:", json.dumps(summary))
