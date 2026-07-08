# Result source tables

Key files:

- `table6_plm_vs_aac.csv`: final matched PLM-vs-AAC source table.
- `paired_stats.csv`: random-CV paired comparison statistics.
- `sensitivity_behavior.csv`: behavior of sensitivity-flagged negative cases under PLM models.
- `plm_classifier_full_aggregate_summary_1_0.csv`: PLM aggregate metrics.
- `plm_classifier_full_per_fold_metrics_1_0.csv`: PLM per-fold metrics.
- `plm_r02a_core_only_addendum_aggregate_summary_1_0.csv`: PLM R02A core-only addendum aggregate metrics.
- `aac_r02a_core_only/`: matched AAC R02A core-only reference outputs.

- `diagnostic/`: public-safe diagnostic/pilot-level R01/R03/R04/R05/R06/R07 traceability CSVs. These support supplementary provenance and reviewer auditability only; they are not primary benchmark evidence. R08 is intentionally absent because no usable metric output was available for public interpretation.

Interpret all R02A rows as descriptive stress-test evidence only. Diagnostic feature-family rows should remain supplementary/contextual and should not be used as primary model-comparison claims.
