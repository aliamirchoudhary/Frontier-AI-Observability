# Source ingestion

## Original payloads

The pinned inventory is reproducible evidence, not a promise that live exports retain the same size. Recheck registry URLs, source rights and checksums when implementing. Preserve source bytes in the restricted landing/archival part of Bronze. Delta record tables add metadata without altering those originals.

| Source | Pinned reference and payloads | Role |
| :--- | :--- | :--- |
| Arena | https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset ; revision `7d2d9009b2ba84383deb6f1b70e66f85b7cda4e7`; text, text_style_control, webdev and agent full Parquet | Historical evaluation observations |
| CooperBench | https://huggingface.co/datasets/CooperBench/team-trajectories ; revision `dd371629174a226ecd251672af315699b77de05d`; cmp-full-solo, cmp-full-coopgit, cmp-full-team and cmp-full-team-noproto tar.gz | Matched study-task outcomes and duration |
| BenchLM | https://benchlm.ai/data/models.json ; https://benchlm.ai/data/benchmarks.json ; https://benchlm.ai/data/pricing.json | Model metadata, benchmark definitions and observed tariffs |
| Epoch | https://epoch.ai/data/all_ai_models.csv | Release and development metadata |

Pinned Arena paths use `https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset/resolve/REVISION/SUBSET/full-00000-of-00001.parquet`. CooperBench paths use `https://huggingface.co/datasets/CooperBench/team-trajectories/resolve/REVISION/ARCHIVE.tar.gz`. The existing [source registry](../../config/source-registry.json) contains exact filenames and original hashes.

Core baseline: **216,373,763 original bytes**, comprising Arena 109,999,378 bytes and CooperBench 106,374,385 compressed bytes. CooperBench decoded member contents total approximately 1,043,616,090 bytes; decoded volume is a separate resource estimate. Supplemental exports previously brought acquisition to roughly 227 MB; their actual new download sizes must be logged. Decimal MB = bytes / 1,000,000.

The demonstrated subsequent publication uses Arena revision `46919c467f7f93d9609b668a283bcd20d87c28bc` and `latest-00000-of-00001.parquet` for text, text_style_control and agent. Its **1,219,849 original bytes** contain 21,896 rows. The manifest records chronology against the baseline. Treat this as a real historical incremental replay, not as a newly collected live batch.

## Acquisition contract

1. Resolve a source revision or capture the response observation time for unversioned exports.
2. Stream into a temporary file; never load an entire archive into laptop memory.
3. Check original byte count and SHA-256; atomically publish only a complete file.
4. Record source URL, revision, source publication bounds, format, byte count, hash and local/cloud artifact identifier.
5. Retain the original format. Parquet-to-CSV expansion is not an acquisition measure.
6. Reuse identical content safely while recording a new acquisition attempt; do not count repeated content as new incremental data.
7. Upload through a supported volume route if a publisher is inaccessible from serverless compute. Verify transferred hashes.

Archive extraction must reject path traversal, absolute paths and links. Extract only required result/evaluation members into a restricted staging area, retain their archive-member names and hashes, and never execute bundled code. Confirm actual evaluation filenames and schemas from the full archives; result samples alone do not prove success.

## Update semantics

Arena: check revisions daily, process changed native publications, and reconcile changed full history periodically. Related text and style-controlled results remain different protocols. Do not pool them as independent observations.

BenchLM and Epoch: collect complete successful snapshots, compare logical content, and keep an observation history. Unchanged logical records do not acquire new Silver timestamps merely because the wrapper build time changed. Current snapshots and history are separate concerns. No historical price is invented before the first observed tariff.

CooperBench: check for corrections or compatible new studies periodically. This static study does not guarantee daily additions. Preserve the publisher alias `gpt-5.5-hao`; do not map it automatically to a public pricing SKU. Zero-filled tokens and cost fields are unmeasured, not proof of zero expenditure.

Missing data is not a deletion signal in partial latest files or failed snapshots. A complete successful replacement snapshot can produce a bounded current-state inactivity event under the documented source policy; earlier observations remain intact. Live batches may be smaller than 1 MB or unchanged. Report that accurately rather than adding irrelevant or duplicate files.

## Privacy and rights

Keep source attribution and separate data licenses from the repository's MIT code license. Arena is labeled CC BY 4.0, CooperBench Apache 2.0 with inherited notices, and BenchLM CC BY-NC 4.0. Review Epoch's requested attribution and current conditions. BenchLM and Free Edition do not support an unrestricted commercial deployment.

Full CooperBench traces and Epoch author/contact fields can contain identifying data. Do not publish full raw payloads, extracts, quarantine payloads, tokens or account screenshots. Silver contains analytical fields and public organization identities, with contact and incidental personal fields dropped. A regex scan is a screening aid, not proof that a dataset is PII-free.
