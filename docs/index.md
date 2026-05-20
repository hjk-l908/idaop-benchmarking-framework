# iDAOP: Antioxidant Peptide Benchmarking Framework

This project page accompanies a manuscript-facing benchmark and evaluation framework for antioxidant peptide prediction studies.
> Release status: This project page currently describes a private pre-submission staging repository. It is not a final public release. Public citation, reuse, DOI, and license information will be finalized only after archival release.

**iDAOP is not a new standalone predictor or web server.** It supports branch-aware dataset governance, transparent AAC baseline evaluation, retained-assignment R02A descriptive stress testing, and a controlled frozen ESM-2 comparison.

## What this repository provides

- Branch-aware dataset manifests
- R1-R10 random-CV and R02A retained-assignment hard-split manifests
- Table 6 PLM-vs-AAC source table
- Paired random-CV statistics
- QC manifests for embedding, split matching, classifier execution, and R02A core-only addendum
- Environment and script inventory

## Main result boundary

Frozen ESM-2 showed some setting-dependent random-CV gains, especially through sensitivity and F1, but did not show stable hard-split superiority over AAC_reference. R02A is descriptive-only because it is based on a retained assignment, has only four fold units, and has few negative test sequences per fold.

## Reviewer quick start

Start with:

1. `reviewer_quick_start.md`
2. `data/branch_summary.csv`
3. `results/table6_plm_vs_aac.csv`
4. `results/paired_stats.csv`
5. `supplementary/R02A_retained_assignment_documentation_1_0.md`
6. `qc/qc_manifest.csv`

## Citation

Citation metadata remains to be finalized in `CITATION.cff` after authors, DOI, and release date are confirmed.
