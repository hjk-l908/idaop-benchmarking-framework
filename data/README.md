# Data manifests

This folder contains public-facing, reviewer-traceable dataset manifests used for the manuscript analyses.

- `branch_manifest.csv`: sequence-level branch manifest for all 959 PLM embedding-input sequences.
- `branch_summary.csv`: branch counts and eligibility summary.
- `full_embedding_input_for_esm2_1_0.csv`: full frozen ESM-2 embedding-input manifest.
- `full_embedding_sequence_order_manifest_1_0.csv`: row-order and sequence-MD5 manifest used to validate embedding order.
- `full_embedding_label_branch_manifest_1_0.csv`: label/branch eligibility manifest.

Challenge-only rows are retained for post hoc scoring/stress-test purposes only and must not appear in training/CV manifests.

## Branch vocabulary note

The canonical public branch vocabulary is `positive_core`, `core_negative`, `negative_sensitivity`, and `challenge_only`. In retained R02A/split files, the legacy value `negative_core` is used in some columns or filenames as a synonym of the canonical `core_negative` branch. This is a naming compatibility note only; it does not imply relabeling, branch reassignment, or a change to headline negative handling.

