# iDAOP: Antioxidant Peptide Benchmarking Framework

This project page accompanies a manuscript-facing benchmark and evaluation framework for antioxidant peptide prediction studies.

> Release status: metadata-repair maintenance release `v1.0.5`, dated 2026-08-26, prepared from GitHub release `v1.0.4` to repair `CITATION.cff` YAML validity and current-facing archival metadata. The scientific datasets, branch assignments, split manifests, model predictions, Table 6 point estimates, and paired-inference results are unchanged from v1.0.4. The previous archived Zenodo release remains v1.0.3 at https://doi.org/10.5281/zenodo.21270655; GitHub release v1.0.4 was published, but its Zenodo archival failed during `CITATION.cff` metadata parsing, so no version-specific v1.0.4 Zenodo DOI was assigned.

**iDAOP is not a new standalone predictor or web server.** It supports branch-aware dataset governance, transparent AAC baseline evaluation, retained-assignment R02A descriptive stress testing, and a controlled frozen ESM-2 comparison.

## What this repository provides

- Branch-aware dataset manifests
- R1-R10 random-CV and R02A retained-assignment hard-split manifests
- Table 6 PLM-vs-AAC source table
- Replicate-level paired random-CV statistics (10 replicate pairs; R02A remains descriptive-only)
- QC manifests for embedding, split matching, classifier execution, and R02A core-only addendum
- Environment and script inventory
- Public-safe diagnostic traceability files for R01/R03/R04/R05/R06/R07 in `results/diagnostic/`
- Release-byte package manifest and SHA-256 inventory

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
7. `results/diagnostic/README.md`
8. `MAINTENANCE_RELEASE_NOTES_v1.0.4.md`

## Citation

Release metadata identify this version as v1.0.5, dated 2026-08-26. The previous archived v1.0.3 Zenodo release remains available at https://doi.org/10.5281/zenodo.21270655; GitHub release v1.0.4 was published, but its Zenodo archival failed during `CITATION.cff` metadata parsing and no version-specific v1.0.4 Zenodo DOI was assigned. `CITATION.cff` identifies version `1.0.5` with release date `2026-08-26`; the version-specific v1.0.5 Zenodo DOI will be added only after Zenodo assigns it and must not be guessed.

## License

Code and command wrappers are released under the MIT License. Public-safe author-prepared benchmark materials and documentation are released under CC BY 4.0, with third-party and restricted-material boundaries described in `DATA_LICENSE.md`.
