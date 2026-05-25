# Diagnostic source-result files

This folder contains public-safe diagnostic and pilot-level source summaries for the iDAOP antioxidant peptide benchmark repository. These files are provided to restore reviewer-facing traceability for staged traditional-baseline and feature-family evidence. They support supplementary provenance, table-value checking, and reviewer auditability; they are not the primary benchmark evidence and should not be used to promote a new predictor claim.

## Scope and interpretation

- The primary transparent baseline remains `AAC_reference + Logistic Regression L2`.
- `AAC_reference + Linear SVM` remains a secondary comparator.
- `AAC_plus_physchem` and `CKSAAP_k1` files are diagnostic feature-family checks only.
- R02A/retained-assignment hard-split rows remain descriptive stress-test evidence, not definitive external validation.
- R06 files are a separate low-dimensional feature-family hard-split diagnostic review and should not be confused with the headline AAC-vs-ESM-2 Table 6 values.
- R07 CKSAAP_k1 files document random-CV diagnostic behavior only.
- R08 hard-split CKSAAP was attempted during development but produced no usable metric output for public interpretation; no R08 file is included here and R08 must not be cited as evidence.
- Challenge-only sequences were not used for training, cross-validation, tuning, model selection, or headline metrics.

## Included public-safe CSV files

| File | Rows | Columns | Diagnostic role |
|---|---:|---:|---|
| `R01_R1_R10_combined_metric_summary.csv` | 16 | 6 | AAC_reference + Logistic Regression L2 repeated random-CV summaries/fold metrics supporting transparent baseline traceability. |
| `R01_R1_R10_replicate_summary_with_R1.csv` | 20 | 19 | AAC_reference + Logistic Regression L2 repeated random-CV summaries/fold metrics supporting transparent baseline traceability. |
| `R01_R2_R10_fold_metrics.csv` | 72 | 28 | AAC_reference + Logistic Regression L2 repeated random-CV summaries/fold metrics supporting transparent baseline traceability. |
| `R01_R2_R10_replicate_summary.csv` | 20 | 19 | AAC_reference + Logistic Regression L2 repeated random-CV summaries/fold metrics supporting transparent baseline traceability. |
| `R03_AAC_model_family_fold_metrics.csv` | 240 | 25 | AAC_reference Logistic Regression L2, Linear SVM, and Random Forest diagnostic model-family source summaries/fold metrics. |
| `R03_AAC_model_family_model_summary.csv` | 6 | 19 | AAC_reference Logistic Regression L2, Linear SVM, and Random Forest diagnostic model-family source summaries/fold metrics. |
| `R03_AAC_model_family_replicate_summary.csv` | 60 | 20 | AAC_reference Logistic Regression L2, Linear SVM, and Random Forest diagnostic model-family source summaries/fold metrics. |
| `R04_R03_randomCV_vs_R04_hardsplit_comparison.csv` | 2 | 22 | Public-safe companion files linking the R03 random-CV AAC model-family review to retained-assignment hard-split diagnostic checks. |
| `R04_hardsplit_AAC_model_family_fold_metrics.csv` | 8 | 27 | Public-safe companion files linking the R03 random-CV AAC model-family review to retained-assignment hard-split diagnostic checks. |
| `R04_hardsplit_AAC_model_family_model_summary.csv` | 2 | 28 | Public-safe companion files linking the R03 random-CV AAC model-family review to retained-assignment hard-split diagnostic checks. |
| `R05_feature_vs_AAC_delta_summary.csv` | 20 | 28 | AAC_reference versus AAC_plus_physchem/terminal/low-dimensional feature-family diagnostic source summaries/fold metrics. |
| `R05_lowdim_feature_family_fold_metrics.csv` | 960 | 27 | AAC_reference versus AAC_plus_physchem/terminal/low-dimensional feature-family diagnostic source summaries/fold metrics. |
| `R05_lowdim_feature_family_model_summary.csv` | 24 | 20 | AAC_reference versus AAC_plus_physchem/terminal/low-dimensional feature-family diagnostic source summaries/fold metrics. |
| `R06_hardsplit_lowdim_feature_fold_metrics.csv` | 16 | 24 | Retained-assignment hard-split diagnostic checks for AAC_reference versus AAC_plus_physchem; not the headline Table 6 AAC-vs-ESM-2 value. |
| `R06_hardsplit_lowdim_feature_model_summary.csv` | 4 | 17 | Retained-assignment hard-split diagnostic checks for AAC_reference versus AAC_plus_physchem; not the headline Table 6 AAC-vs-ESM-2 value. |
| `R06_hardsplit_lowdim_feature_vs_AAC_delta.csv` | 2 | 23 | Retained-assignment hard-split diagnostic checks for AAC_reference versus AAC_plus_physchem; not the headline Table 6 AAC-vs-ESM-2 value. |
| `R07_CKSAAP_minimal_fold_metrics.csv` | 320 | 23 | Minimal CKSAAP_k1 diagnostic source summaries/fold metrics and deltas versus AAC_reference; diagnostic only. |
| `R07_CKSAAP_minimal_model_summary.csv` | 8 | 20 | Minimal CKSAAP_k1 diagnostic source summaries/fold metrics and deltas versus AAC_reference; diagnostic only. |
| `R07_CKSAAP_vs_AAC_delta_sensplus.csv` | 2 | 10 | Minimal CKSAAP_k1 diagnostic source summaries/fold metrics and deltas versus AAC_reference; diagnostic only. |


## Public-safety status

Before release, these CSV files were screened with the private-path, credential, draft-marker, and internal-archive search patterns documented in `docs/repo_safety_search_commands.md`. No matches were detected in the candidate CSV contents at the time of packaging.

Repeat the safety search after merging this folder into the full repository, because other repository files may still contain unreleased local development traces.

## Recommended manuscript/supplement routing

- S3: Use these files as the reviewer-facing staged baseline/diagnostic evidence package for R01/R03/R04/R05/R06/R07. Keep diagnostic rows clearly separated from primary baseline evidence.
- S4: Use fold-level files from this folder only where they support AAC traditional-baseline traceability. PLM matched-comparison files remain in the PLM/QC release folders.
- S7: Add the SHA-256 entries for these files to the repository checksum inventory.

## Do not include

Do not publish the original internal server-process archive or local run logs. Do not add raw files that contain server paths, usernames, development notes, or command histories. R08 must remain described as attempted but not interpreted because no usable metrics were produced.
