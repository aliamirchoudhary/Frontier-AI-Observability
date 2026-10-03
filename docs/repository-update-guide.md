# Installing the replacement package

1. Extract the ZIP outside your Git working directory.
2. Preserve your `.git` directory and any independent work you have added.
3. Replace the existing `data/samples/` directory with the packaged version. This removes superseded Arena sample files and installs the matching manifest. Do not merge old and new sample directories.
4. Replace the old proposal named `proposals/Phase 1 proposal.docx` with `proposals/Phase-1-Proposal.docx`. The README links to the new path.
5. Copy the remaining package files into the repository root, replacing matching files.
6. Install the local verification dependency and run `python tools/verify_samples.py`.
7. Review `git status` and `git diff`, then stage and commit the replacement. No remote changes are made by this package.

The cloud pipeline remains planned. The package contains proposal materials, verified samples, source documentation and a local sample verifier, not completed Bronze/Silver/Gold jobs. Large source archives, secrets and restricted raw data are excluded.
