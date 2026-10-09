# Transfer and network readiness

Read [GitHub acquisition](github-acquisition.md). Source requests execute on Actions; Databricks outbound publisher access is no longer a prerequisite for this selected route. This architecture does not satisfy the original source-call-location rule unless the instructor accepts the change.

Task 02 tests the exact workspace's supported authentication and Files API with a tiny synthetic file, then cloud readback and managed Delta MERGE. Verify supported API scope/privileges and a writable approved volume. A generic Databricks API example does not prove this Free Edition account supports the route. No raw baseline transfer until the tiny test passes.

Task 03 verifies every publisher endpoint and redirect from the GitHub runner. HTTP 200 metadata is insufficient: full native payload download, hash validation and upload/readback must complete. Record redacted endpoint hosts, status/exception category, elapsed time, bytes and workflow run/code SHA. Distinguish DNS/network errors, authentication, rate limits, missing revisions and parse failures. Use verified TLS, bounded retries and buffers.

No tunnel, proxy, TLS bypass or VPN is needed or authorized. Actions collects the source openly as a separate acquisition service. If authentication/volume upload is unsupported, stop instead of assuming that Actions solves every restriction. Instructor acceptance and technical route readiness are separate statuses.
