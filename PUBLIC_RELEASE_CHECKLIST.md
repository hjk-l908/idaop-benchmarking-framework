# Public release checklist

This checklist records the public GitHub release, licensing, Zenodo archival, and v1.0.4 maintenance-candidate status for the iDAOP repository.

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
- [ ] Confirm whether large binary embedding files should remain in GitHub, Zenodo, or both.

## Pending v1.0.4 release actions

- [ ] Review and approve the `v1.0.4-rc1` maintenance candidate.
- [ ] Commit and push the candidate repository state.
- [ ] Before tagging, set `CITATION.cff` `version` to `1.0.4`, replace the candidate `message`, and add `date-released: YYYY-MM-DD`.
- [ ] Create GitHub release `v1.0.4`.
- [ ] Archive GitHub release `v1.0.4` through Zenodo.
- [ ] After Zenodo assigns it, add the actual final v1.0.4 DOI and release date to current-facing metadata; do not guess the DOI.
- [ ] Regenerate `metadata/package_file_manifest.csv` and `metadata/SHA256SUMS.txt` after every final metadata edit.
- [ ] Record the SHA-256 of `metadata/SHA256SUMS.txt` in the GitHub Release body or another external release audit record.
- [ ] Extract the downloaded GitHub and Zenodo release archives and run `python scripts/verify_package_checksums.py` inside each extracted tree; do not treat a GitHub-generated archive-file hash as a stable identifier.
- [ ] Update manuscript Data availability and Additional file 7 only after final archive verification.

## Release citation

- Current archived GitHub release: `v1.0.3` (https://github.com/hjk-l908/idaop-benchmarking-framework/releases/tag/v1.0.3)
- Current archived Zenodo DOI: https://doi.org/10.5281/zenodo.21270655
- Maintenance candidate: `v1.0.4-rc1`
- Candidate prepared: 2026-07-27
- Independent audit reconciliation prepared: 2026-08-05
- v1.0.4 DOI and release date: not yet assigned
