# Integrate this pack into the repository

Copy the CONTENTS of public/ into the existing root; do not commit the wrapper or delivery guide. Preserve existing project files and .git. Review any existing AGENTS.md before merging the supplied guardrails; preserve unrelated relevant instructions. Replace docs/phase-2 with this updated set so obsolete Databricks-native acquisition instructions do not linger.

The repository keeps reviewed documentation, notebook/collector code, source contracts, small permitted samples, proposal, notices and sanitized evidence. Full raw files, archives, extracts, quarantine content, secrets, credential files, venvs and unsanitized outputs are excluded. Operators keep operational prompt guides outside the repository and workspace.

Add these patterns to the existing .gitignore after checking current conventions; do not replace it blindly:

```gitignore
.venv/
__pycache__/
.env
.env.*
!.env.example
.databrickscfg
raw/
.tmp/
.staging/
working/
*.tar.gz
*.log
```

Raw download paths must be explicit and ignored rather than ignoring every JSON/CSV/Parquet (representative samples are allowed). Review notebook outputs and credential/config files manually. Ignore rules do not untrack history or restrict agent reading. If sensitive files are already tracked, stop for a separate remediation decision.

Link README to docs/phase-2/README.md and describe status accurately. Do not overwrite Phase 1 proposal to imply that its original source-call route remains the implemented route; add the selected architecture decision and pending instructor acceptance in current docs.
