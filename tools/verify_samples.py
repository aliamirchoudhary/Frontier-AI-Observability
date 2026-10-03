"""Verify repository sample bytes, row counts and publication order locally."""
from pathlib import Path
import hashlib
import json
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / "data/samples/manifest.json").read_text())
errors = []
for item in manifest["samples"]:
    path = (ROOT / item["path"]).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file():
        errors.append(f"Missing or invalid path: {item['path']}")
        continue
    data = path.read_bytes()
    if len(data) != item["bytes"]:
        errors.append(f"Byte size mismatch: {item['path']}")
    if hashlib.sha256(data).hexdigest() != item["sha256"]:
        errors.append(f"Checksum mismatch: {item['path']}")
    if path.suffix == ".parquet":
        table = pq.read_table(path)
        if table.num_rows != item["rows"]:
            errors.append(f"Row count mismatch: {item['path']}")
        if item["path"].startswith("data/samples/incremental/arena/"):
            name = path.name.split("-latest")[0] + "-full-00000-of-00001.parquet"
            source = next(x for x in manifest["sources"] if x["name"] == name)
            publications = [str(x) for x in table["leaderboard_publish_date"].to_pylist()]
            if not publications or min(publications) <= source["maximum_publication"]:
                errors.append(f"Increment does not follow baseline: {item['path']}")
    elif path.suffix == ".json":
        json.loads(data)
core_bytes = sum(x["original_bytes"] for x in manifest["sources"])
increment_bytes = sum(x["bytes"] for x in manifest["samples"]
                      if x["kind"] == "Unchanged complete native source file")
if core_bytes != manifest["full_baseline_original_bytes"] or core_bytes < 200_000_000:
    errors.append("Invalid core source inventory total")
if increment_bytes != manifest["incremental_original_bytes"] or increment_bytes < 1_000_000:
    errors.append("Invalid native incremental payload total")
if errors:
    raise SystemExit("\n".join(errors))
print(f"Verified {len(manifest['samples'])} public sample files.")
print(f"Core source inventory: {core_bytes:,} bytes; full payloads are not bundled.")
print(f"Native incremental payload: {increment_bytes:,} bytes.")
print("This validates samples and the recorded source inventory, not a cloud pipeline.")
