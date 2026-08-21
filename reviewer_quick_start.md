# Reviewer quick start for iDAOP

This repository is organized to let reviewers trace the manuscript's key tables, branch decisions, and controlled comparison results without rerunning the full computational workflow.

**iDAOP is a benchmark and evaluation framework for antioxidant peptide prediction studies, not a new standalone predictor or web server.**

## 1. Branch policy

Open `data/branch_summary.csv` and `data/branch_manifest.csv`.

Expected branch counts:

- positive_core = 899
- core_negative = 29
- negative_sensitivity = 3
- challenge_only = 28

Challenge-only sequences are embedded for post hoc stress-testing only and are not present in training/CV split manifests.

## 2. Table 6 source

Open `results/table6_plm_vs_aac.csv`.

This file contains the final matched PLM-vs-AAC comparison table, including completed R02A hard-split core_only rows. The hard-split rows are descriptive only.

## 3. Random-CV paired statistics

Open `results/paired_stats.csv`.

For the v1.0.4 candidate, random-CV paired inference uses the 10 sampling replicates as the inferential unit after averaging the four folds within each replicate. The archived v1.0.3 `paired_stats.csv` is retained only in that historical release as fold-level provenance. The corrected LR_L2 core-only MCC delta is +0.059 with two-sided Wilcoxon p = 0.064 and bootstrap 95% CI +0.006 to +0.109; the sensitivity-augmented LR_L2 MCC delta is +0.040 with p = 0.232 and CI -0.020 to +0.100. These rows support a setting-dependent, non-stable PLM effect rather than a stable-superiority claim.

## 4. R02A retained-assignment status

Open `supplementary/R02A_retained_assignment_documentation_1_0.md` and `splits/PILOT_R02A_sequence_cluster_hard_split_assignments.csv`.

R02A is a retained-assignment hard-split stress test. The original cluster-generation command was not recovered, so this split is not presented as a fully regenerable clustering protocol.

## 5. QC evidence

Open `qc/qc_manifest.csv` for a summary, then inspect JSON files in `qc/` as needed.

## 6. Local validation

Run:

```bash
python scripts/validate_repository.py
```

Expected output:

```text
VALIDATION_STATUS: PASS
```
