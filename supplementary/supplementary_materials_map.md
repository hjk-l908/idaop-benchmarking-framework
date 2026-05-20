# Supplementary materials map

| File | Recommended title | Contents | Status in this Phase 2 repository |
|---|---|---|---|
| S1 | Branch manifest and eligibility table | positive_core, core_negative, negative_sensitivity, challenge_only counts and allowed/prohibited use | Implemented in `data/branch_manifest.csv` and `data/branch_summary.csv` |
| S2 | R02A retained assignment and split details | retained source assignment, recorded rule, R02A sensplus/core_only manifests, limitation wording | Implemented in `splits/` and `supplementary/R02A_retained_assignment_documentation_1_0.md` |
| S3 | R01-R08 baseline evidence package | baseline decision lock and random-CV/hard-split summaries | Not fully populated in this Phase 2 repo; integrate final reviewer-facing simplified evidence file when ready |
| S4 | Per-fold AAC and PLM metrics | per-fold metrics for AAC_reference and frozen ESM-2 comparisons, including R02A core_only addendum | PLM per-fold and AAC R02A core-only files included in `results/` |
| S5 | QC and run manifests | split matching validation, embedding QC, classifier output QC, checksum manifest | Included in `qc/` and `metadata/SHA256SUMS.txt` |
| S6 | Sensitivity-negative behavior | behavior of VLDTDY, LKALPMH, and IQKVAGTW | Included in `results/sensitivity_behavior.csv` |
| S7 | Code and environment inventory | package versions, command wrappers, classifier scripts, R02A retained-assignment note | Included in `environment/`, `scripts/`, `commands/`, and `supplementary/` |
