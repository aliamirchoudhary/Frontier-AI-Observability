# Repository readiness record (Task 01)

**Date:** 2026-10-09 · **Scope:** local repository readiness only. No workflow dispatch, no source download, no Git write, no cloud provisioning and no dependency installation was performed for this record. Cloud pipeline success is **not** claimed anywhere in this file.

## 1. Observed environment

| Item | Observed value |
| :--- | :--- |
| Repository root | `D:/Project/Frontier AI Observatory/Frontier-AI-Observability` (matches approved path) |
| Remote | `https://github.com/aliamirchoudhary/Frontier-AI-Observability.git` |
| OS / shell | Windows NT 10.0.26200 · PowerShell 5.1 |
| Git | 2.51.0.windows.1 available |
| Python | 3.12.3 present on this machine, **not required** by this task; `pyarrow` and `pyyaml` are **not** installed |
| Java / Spark | absent locally (expected; no local Spark is required) |
| Branch at start | `phase2/repository-readiness` @ `adba742cefb8fa853cb8089a61dca544f3f486d2` (approved `dev` baseline, same SHA as `origin/dev`) |
| Working tree at start | clean; no staged or unrelated changes |
| Operator identity | `aliamirchoudhary <aliamirchoudhary@gmail.com>` (Ali) |

## 2. What exists versus what is planned

| Component | State |
| :--- | :--- |
| Reviewed docs, Phase 1 proposal, source registry, public samples, notices, `tools/verify_samples.py` | **Existing** and unchanged by this task except README links |
| `docs/phase-2/` specification pack | **Existing**; now linked from README |
| `src/` (collector, contracts, transforms) | **PLANNED skeleton** — every entry point raises `NotImplementedError`; no schema fields defined |
| `notebooks/` (two thin notebooks) | **PLANNED skeleton** — parameter contract only; never executed anywhere |
| `.github/workflows/acquire-sources.yml` | **PLANNED placeholder** — `workflow_dispatch` only, permissions `contents: read`, job always exits non-zero so a dispatch cannot appear successful |
| Staging volume, Bronze/Silver Delta tables, operational tables | **Not created** (no workspace access exercised in this task) |
| Task 02 authentication / tiny transfer | **Blocked** — needs human-set GitHub secrets and workspace identifiers |
| Instructor acceptance of the Actions route | **Pending** (recorded separately from technical status) |

## 3. Runner / cloud dependency plan (no local installation performed)

| Where | Plan |
| :--- | :--- |
| GitHub Actions runner | Python 3.x on the standard hosted runner; prefer the standard library (`urllib.request`, `hashlib`, `json`, `tarfile`) for acquisition so no third-party pin is needed. Any added HTTP client must be version-pinned in a dedicated runner requirements file at Task 03, after review. No paid runners or storage. |
| Local sample verifier (future runner use) | `python -m pip install -r requirements.txt` then `python tools/verify_samples.py` from the repository root (`pyarrow>=18,<24`). **Not executed in Task 01:** `pyarrow` is not installed on this machine and installing dependencies was out of scope for this task. Absence of local Python/venv is not a failure. |
| Databricks Free Edition | Managed Spark/Delta only — no `pip` installation of Spark/Delta, Spark Connect-compatible DataFrame/SQL APIs, no RDDs or DBFS mounts. Notebooks declare parameters from the [execution guide](execution-guide.md); any permitted notebook library is declared in an environment manifest at Task 02+ before first use. |
| Sample data | The repository's small reviewed samples are the only local data; full baselines live outside Git (see [source-ingestion.md](source-ingestion.md)). |

## 4. Checks executed for this task (local, with outcomes)

| Check | Outcome |
| :--- | :--- |
| `git --no-optional-locks status` before edits | clean tree on `phase2/repository-readiness` @ `adba742…` — PASS |
| Root, remote, identity, branch/baseline inspection | all match the authorized values — PASS |
| README, proposal (`Phase-1-Proposal.docx` text extracted for review), `config/source-registry.json`, `data/samples/*`, `THIRD_PARTY_NOTICES.md`, `tools/verify_samples.py` inspected | PASS; no unrelated file modified |
| README relative links resolve to existing files | PASS (checked programmatically; see report) |
| New Python scaffolds compile (`python -m py_compile`, syntax only — no imports executed) | PASS |
| Workflow YAML parsed | **not run** — no YAML parser available locally (`pyyaml` absent); manual review pending |
| `tools/verify_samples.py` | **not run** — `pyarrow` not installed; command recorded in §3 for future runner execution |
| Cloud readiness (Task 02 tiny upload/readback) | **not attempted** — requires human-set secrets and workspace identifiers |

## 5. Awaiting the human / later tasks

1. Review and accept the proposed file list from the Task 01 report (nothing is staged or committed).
2. Task 02: provide approved GitHub secrets (`DATABRICKS_HOST`, supported credential secret, approved volume path variables) and confirm the Free Edition workspace identifier, then run the tiny upload/readback test.
3. Instructor acceptance of the Actions acquisition route (recorded separately from technical readiness).
4. Run `python tools/verify_samples.py` in an environment where `requirements.txt` is installed.

## 6. Unresolved questions

1. Which Free Edition workspace/catalog/schema/volume names are approved for staging, Bronze, Silver and ops tables?
2. Which supported credential type does this workspace permit from Actions (Task 02 decides; no token is to be requested in chat or code)?
3. Should the runner use pure standard library for acquisition, or may a pinned HTTP client be added after Task 02 review?
