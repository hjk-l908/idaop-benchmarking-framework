# Data manifests

This folder contains public-facing, reviewer-traceable dataset manifests used for the manuscript analyses.

- `branch_manifest.csv`: sequence-level branch manifest for all 959 PLM embedding-input sequences.
- `branch_summary.csv`: branch counts and eligibility summary.
- `full_embedding_input_for_esm2_1_0.csv`: full frozen ESM-2 embedding-input manifest.
- `full_embedding_sequence_order_manifest_1_0.csv`: row-order and sequence-MD5 manifest used to validate embedding order.
- `full_embedding_label_branch_manifest_1_0.csv`: label/branch eligibility manifest.

Challenge-only rows are retained for post hoc scoring/stress-test purposes only and must not appear in training/CV manifests.
