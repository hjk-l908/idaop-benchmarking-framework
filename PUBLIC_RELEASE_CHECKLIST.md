# Public release checklist

This checklist records the public GitHub release, licensing, Zenodo archival, the v1.0.4 maintenance-release workflow, and the post-v1.0.4 v1.0.5 archival-repair workflow for the iDAOP repository.

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
- [x] Large binary embedding files remain in GitHub; inclusion in the planned v1.0.4 Zenodo archive was not completed because Zenodo archival failed.

## v1.0.4 release outcome

- [x] Review and approve the `v1.0.4-rc1` maintenance candidate.
- [x] Apply the final pre-release metadata conversion on `maintenance-v1.0.4-rc1`, including `CITATION.cff` version/message/date-released and confirmed stale current-facing release wording.
- [x] Regenerate `metadata/package_file_manifest.csv` and `metadata/SHA256SUMS.txt` after the final v1.0.4 pre-release metadata edits.
- [x] Commit and push the final pre-release repository state and confirm repository validation, checksum verification, and `git diff --check` pass.
- [x] Mark the pull request ready for review and merge `maintenance-v1.0.4-rc1` into `main`.
- [x] Confirm the merged `main` commit and validation checks before release.
- [x] Create GitHub release/tag `v1.0.4` from validated merged `main` commit `35d64da`.
- [x] Trigger Zenodo archival for GitHub release `v1.0.4`; Zenodo received the release, but archival failed during `CITATION.cff` metadata parsing.
- [x] Confirm that no version-specific v1.0.4 Zenodo DOI was assigned; do not guess or fabricate one.
- [x] Record the validated v1.0.4 GitHub release state: `VALIDATION_STATUS: PASS`, `CHECKSUM_STATUS: PASS`, `TOTAL_ENTRIES: 131`, `CHECKED_FILES: 131`.
- [x] Record the v1.0.4 GitHub Release SHA-256 of `metadata/SHA256SUMS.txt`: `e69c4b2384d5af255a032da027f938b1d311ccdd4c63cc461539b453390134b30`.
- [x] Record that cross-archive GitHub/Zenodo verification for v1.0.4 could not be completed because no Zenodo archive was created.
- [ ] Reviewer-facing Supplementary File S4 refresh remains deferred until the successful archival repair release hashes are locked.
- [ ] Update manuscript Data availability and Additional file 7 only after successful archival verification of the repair release.

## v1.0.4 release citation

- Previous Zenodo-archived GitHub release: `v1.0.3` (https://github.com/hjk-l908/idaop-benchmarking-framework/releases/tag/v1.0.3)
- Previous archived Zenodo DOI: https://doi.org/10.5281/zenodo.21270655
- GitHub maintenance release: `v1.0.4`
- GitHub release date: 2026-08-21
- v1.0.4 version-specific Zenodo DOI: not assigned; Zenodo archival failed during `CITATION.cff` metadata parsing; do not guess.

## Post-v1.0.4 Zenodo archival repair / v1.0.5

- [x] Diagnose the v1.0.4 Zenodo failure as an unterminated double-quoted `message` scalar in `CITATION.cff`.
- [x] Apply and independently validate the minimal closing-quote repair before release-version conversion.
- [x] Prepare `CITATION.cff` for v1.0.5 with version `1.0.5` and release date `2026-08-26`.
- [x] Update `DATA_LICENSE.md` current-release wording to v1.0.5 / 2026-08-26.
- [x] Update `README.md` current-facing release status and archival workflow while preserving v1.0.4 historical provenance.
- [x] Update `docs/index.md` current-facing release metadata while preserving the v1.0.4 maintenance-release notes reference.
- [x] Record the v1.0.4 archival failure outcome and v1.0.5 repair workflow in this checklist.
- [x] Record the v1.0.5 pre-merge validation baseline at commit `c9eaee563afe2141d1e4d65405d9cc6845d760f4`: GitHub Actions workflow #30 passed `VALIDATION_STATUS: PASS` and `CHECKSUM_STATUS: PASS` (`TOTAL_ENTRIES: 131`; `CHECKED_FILES: 131`).
- Inventory freeze rule: after this checklist text is finalized, regenerate `metadata/package_file_manifest.csv` and `metadata/SHA256SUMS.txt` exactly once more; no tracked metadata edits are permitted afterward unless the inventories are regenerated again.
- Final validation gate: the frozen closure commit must pass repository validation, checksum verification, `git diff --check`, and final CFF/YAML validation; completion is evidenced by the closure commit and GitHub Actions/PR records rather than by a post-validation edit to this checklist.
- [ ] Commit and push the repair branch, open/review the pull request, and merge only after validation passes.
- [ ] Create GitHub release/tag `v1.0.5` from the validated merged `main` commit.
- [ ] Archive GitHub release `v1.0.5` through Zenodo and obtain the version-specific DOI.
- [ ] After Zenodo assigns it, add the actual v1.0.5 DOI to current-facing metadata; do not guess.
- [ ] Verify downloaded GitHub and Zenodo v1.0.5 archives against the final inventory and checksums.
- [ ] Update reviewer-facing Supplementary File S4 and manuscript data-availability materials only after successful final archive verification.

## v1.0.5 release citation

- Release version: `v1.0.5`
- Release date: 2026-08-26
- v1.0.5 version-specific Zenodo DOI: pending archival assignment; do not guess.
