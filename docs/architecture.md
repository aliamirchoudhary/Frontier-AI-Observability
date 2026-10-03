# Proposed architecture

An automated collector acquires original source payloads and records their revisions and checksums. Bronze retains native Arena Parquet, CooperBench tar.gz, BenchLM JSON and Epoch CSV. Archive JSON members are staged safely without changing values before Spark processing.

Silver normalizes units and observation fields, validates counts, drops unnecessary personal fields, and reviews model aliases. Grain is defined separately for model configurations, evaluation observations, benchmark versions, tariffs, releases, study tasks and agent traces. Conflicting records and unresolved aliases remain visible for review.

Gold connects facts through model configuration, organization, benchmark, methodology and time dimensions. Agent facts also use study setting and task dimensions. Comparable result series remain separate. Price joins require compatible configurations and appropriate observation times.

The three proposed dashboard views compare capability with estimated workload cost, coordination success with duration, and published capability over time. Measurement coverage and source provenance accompany each view. Aggregate source scores are not task-level evidence for bootstrapping, and published tariffs are not measured agent bills.

The cloud pipeline and dashboard remain planned. Later implementation will add explicit Spark contracts, replay-safe Delta writes, backfills and operational audit evidence.
