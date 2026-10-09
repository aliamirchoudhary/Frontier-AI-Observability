"""PLANNED — source acquisition on a GitHub Actions runner. Not implemented.

Status: Task 01 scaffold only. This module performs no download, hash or
manifest work; every entry point raises NotImplementedError.

Specification (binding when implemented):
  docs/phase-2/source-ingestion.md   — acquisition contract, update semantics
  docs/phase-2/github-acquisition.md — transfer contract steps 1-8
  docs/phase-2/network-readiness.md  — Task 02 auth/tiny-transfer gate,
                                       Task 03 endpoint gate

Required behavior recorded here so the scaffold cannot be mistaken for a
working collector:
  - resolve a pinned source revision, or capture the observation time for
    unversioned exports;
  - stream into a temporary file; never buffer a whole archive in memory;
  - verify original byte count and SHA-256, then publish atomically;
  - record URL, revision, publication bounds, format, bytes, hash, artifact id;
  - retain the native format; a re-export is not an acquisition;
  - record a new acquisition attempt when identical content is reused without
    counting it as new incremental data.
"""


def planned_only(*_args, **_kwargs):
    """Every acquisition entry point until Task 03 is implemented."""
    raise NotImplementedError(
        "PLANNED: acquisition is not implemented. "
        "See docs/phase-2/source-ingestion.md and docs/phase-2/github-acquisition.md."
    )
