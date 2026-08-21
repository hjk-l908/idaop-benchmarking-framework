# iDAOP: Antioxidant Peptide Benchmarking Framework

This project page accompanies a manuscript-facing benchmark and evaluation framework for antioxidant peptide prediction studies.

> Release status: maintenance release `v1.0.4`, dated 2026-08-21, prepared from archived release `v1.0.3` to correct archive-byte checksum consistency, stale current-status metadata, and the random-CV paired-inference unit. The release `results/paired_stats.csv` uses 10 replicate-level pairs for random-CV inference. The previous archived Zenodo release is v1.0.3 at https://doi.org/10.5281/zenodo.21270655; the version-specific v1.0.4 Zenodo DOI will be added only after Zenodo assigns it.

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

Release metadata identify this version as v1.0.4, dated 2026-08-21. The previous archived v1.0.3 Zenodo release remains available at https://doi.org/10.5281/zenodo.21270655. `CITATION.cff` identifies version `1.0.4` with release date `2026-08-21`; the version-specific v1.0.4 Zenodo DOI will be added only after Zenodo assigns it and must not be guessed.

## License

Code and command wrappers are released under the MIT License. Public-safe author-prepared benchmark materials and documentation are released under CC BY 4.0, with third-party and restricted-material boundaries described in `DATA_LICENSE.md`.
