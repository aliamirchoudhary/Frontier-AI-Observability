"""PLANNED — native-byte upload from Actions to Databricks staging. Not implemented.

Status: Task 01 scaffold only. No Files API call, credential read or volume
write exists here; every entry point raises NotImplementedError.

Specification (binding when implemented):
  docs/phase-2/github-acquisition.md — transfer contract steps 1-8
  docs/phase-2/network-readiness.md  — Task 02 proves supported authentication
                                       and tiny upload/readback BEFORE any raw
                                       baseline transfer

Required behavior recorded here so the scaffold cannot be mistaken for a
working uploader:
  - credentials come from human-set GitHub secrets (DATABRICKS_HOST, a
    supported token/credential secret, approved volume path variables); never
    requested in chat, scripts or notebook cells; billing stays disabled;
  - write to a batch-specific volume path with overwrite disabled; reuse an
    existing finalized file only after a verified hash match;
  - verify stored bytes by readback/checksum, not by PUT success or length;
  - publish manifest and ready marker last; readers require manifest plus
    checksum match, not marker existence alone;
  - an incomplete upload is never consumable and is never marked ready.
"""


def planned_only(*_args, **_kwargs):
    """Every upload entry point until Task 02 is implemented."""
    raise NotImplementedError(
        "PLANNED: staging upload is not implemented. "
        "See docs/phase-2/github-acquisition.md and docs/phase-2/network-readiness.md."
    )
