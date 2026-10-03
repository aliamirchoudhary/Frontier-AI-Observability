# Source registry guide

The machine-readable registry is [config/source-registry.json](../config/source-registry.json). It records exact acquisition URLs, pinned full payloads, original byte sizes and checksums, record grains, collection patterns, analytical purpose, reuse conditions and privacy boundaries.

Arena supplies historical and subsequent observations. CooperBench supplies a complete historical coordination study and revisions when published. BenchLM and Epoch support content comparison of snapshots. No source is assumed to publish every day, and an unchanged download is not a new analytical observation.

Model and organization dimensions connect sources conservatively. Versions, reasoning settings, harnesses and deployment modes are preserved. CooperBench's publisher-reported Azure deployment alias remains a source identity; it is not forced onto a public pricing SKU.

Missing records are marked unavailable only after complete successful snapshots confirm their absence. Failed downloads cannot trigger removals. Public samples remain small, while complete payloads remain outside Git.
