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

These rows support the statement that PLM gains are setting-dependent: LR_L2 core_only random-CV MCC improves modestly, while LinearSVM primarily shifts toward sensitivity/F1 with lower specificity.

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
