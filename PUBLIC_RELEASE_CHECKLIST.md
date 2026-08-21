# Public release checklist

This checklist records the public GitHub release, licensing, Zenodo archival, and v1.0.4 maintenance-release workflow for the iDAOP repository.

## Completed before public release

- [x] Repository name and GitHub URL confirmed.
- [x] Main branch synchronized with the manuscript-facing release-candidate repository state.
- [x] `results/diagnostic/` restored with public-safe R01/R03/R04/R05/R06/R07 traceability files.
- [x] No R08 metric file included in `results/diagnostic/`.
- [x] Author names/order updated in `CITATION.cff`; ORCID identifiers are not listed in this repository snapshot per author-side decision.
- [x] Code license selected: MIT License.
- [x] Public-safe benchmark-materials license selected: CC BY 4.0, with third-party/restricted-source exclusions documented in `DATA_LICENSE.md`.
- [x] Current-tree safety review found no intentionally distributed source PDFs, validation PDFs, restricted source archives, FASTA/FA raw source files, CIF files, credentials, API tokens, or concrete private execution paths intended for release.
- [x] Scientific boundary retained: iDAOP is a benchmark/evaluation framework, not a standalone predictor or web server.
- [x] Scientific boundary retained: frozen ESM-2 is a controlled comparator and does not support a stable-superiority claim over AAC_reference.

## Completed release and candidate-preparation actions

- [x] Create and archive GitHub release `v1.0.3`.
- [x] Confirm v1.0.3 Zenodo DOI: https://doi.org/10.5281/zenodo.21270655.
- [x] Prepare maintenance candidate `v1.0.4-rc1` with LF line-ending policy and candidate-byte checksum regeneration.
- [x] Add checksum verification script and GitHub Actions checksum validation step.
- [x] Remove stale current-status statements that incorrectly described the v1.0.3 DOI as pending.
- [x] Correct random-CV paired inference in `results/paired_stats.csv` to use 10 replicate-level pairs after within-replicate fold averaging; preserve R02A as descriptive-only.
- [x] Confirm that the paired-inference correction changes p values/confidence intervals only and does not rerun models or change Table 6 point estimates.
- [x] Large binary embedding files will remain in GitHub and will also be included in the v1.0.4 Zenodo archival (both).

## Pending v1.0.4 release actions

- [x] Review and approve the `v1.0.4-rc1` maintenance candidate.
- [x] Apply the final pre-release metadata conversion on `maintenance-v1.0.4-rc1`, including `CITATION.cff` version/message/date-released and any confirmed stale current-facing release wording; do not guess the v1.0.4 DOI.
- [x] Regenerate `metadata/package_file_manifest.csv` and `metadata/SHA256SUMS.txt` after the final pre-release metadata edits.
- [ ] Commit and push the final pre-release repository state and confirm repository validation, checksum verification, and `git diff --check` all pass.
- [ ] Mark the pull request ready for review only after the final pre-release checks pass, then merge `maintenance-v1.0.4-rc1` into `main`.
- [ ] Confirm the merged `main` commit and its validation checks before creating the release.
- [ ] Create GitHub release/tag `v1.0.4` from the validated merged `main` commit.
- [ ] Archive GitHub release `v1.0.4` through Zenodo.
- [ ] After Zenodo assigns it, add the actual final v1.0.4 DOI and release date to current-facing metadata; do not guess the DOI.
- [ ] Regenerate `metadata/package_file_manifest.csv` and `metadata/SHA256SUMS.txt` after every final metadata edit.
- [ ] Record the SHA-256 of `metadata/SHA256SUMS.txt` in the GitHub Release body or another external release audit record.
- [ ] Extract the downloaded GitHub and Zenodo release archives and run `python scripts/verify_package_checksums.py` inside each extracted tree; do not treat a GitHub-generated archive-file hash as a stable identifier.
- [ ] Regenerate the reviewer-facing Supplementary File S4 source inventory after the final v1.0.4 repository hashes are locked, so its `results/paired_stats.csv` hash matches the released file.
- [ ] Update manuscript Data availability and Additional file 7 only after final archive verification.

## Release citation

- Previous archived GitHub release: `v1.0.3` (https://github.com/hjk-l908/idaop-benchmarking-framework/releases/tag/v1.0.3)
- Previous archived Zenodo DOI: https://doi.org/10.5281/zenodo.21270655
- Release version: `v1.0.4`
- Initial maintenance candidate prepared: 2026-07-27
- Independent audit reconciliation prepared: 2026-08-05
- Paired-inference correction prepared: 2026-08-10
- Release date: 2026-08-21
- v1.0.4 version-specific Zenodo DOI: pending archival assignment; do not guess.
