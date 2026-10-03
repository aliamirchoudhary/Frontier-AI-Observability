# Data attribution and licence notices

The [MIT licence](LICENSE) covers original project code. It does not relicense third-party data.

## Arena

Publisher: Arena / lmarena-ai. Source: https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset

The dataset is labelled [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Credit Arena in charts and derived exports. Full-load samples select source rows and reserialize them as Parquet; source values and schemas are preserved, while bytes differ. Incremental Parquet samples are unchanged complete native source files. Revisions, selections and checksums are in the sample manifest. Model licence labels are separate from the dataset licence.

## CooperBench

Publisher: CooperBench. Source: https://huggingface.co/datasets/CooperBench/team-trajectories

The original coordination-study dataset card specifies [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0). Public samples are unchanged result JSON members from the four complete study settings. Retain source attribution and any applicable notices. Code, patches and text inherited from benchmark repositories may retain additional rights and notices. Complete archives, raw prompts and unreviewed traces are not redistributed in this repository.

## BenchLM

Publisher: BenchLM.ai. Source: https://benchlm.ai/data

Website JSON downloads are [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). The supplied JSON samples select representative items and retain source-level attribution and notices. Noncommercial analysis and attributed outputs must preserve these terms. Commercial use requires a suitable licence or replacement source. Underlying publisher measurements retain their own rights.

## Epoch AI

Publisher: Epoch AI. Source: https://epoch.ai/data/ai-models

Retain the attribution and applicable reuse conditions published with the source. The complete CSV is not included in public samples because author and free-text fields can contain personal information. Silver will omit those unnecessary fields; required source credits remain separate.

## Excluded sources

Artificial Analysis, OpenRouter payloads and SWE-bench submission traces are outside this public sample package. Adding a source requires review of its own access and redistribution terms.
