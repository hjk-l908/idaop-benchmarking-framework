# v2.1 administrative and synchronization patch summary

This patch addresses the non-scientific residual items identified during the Claude Round 1 closure verification. It does not alter Table 6, headline metric values, branch membership, R08 exclusion, or the benchmark/evaluation-framework claim boundary.

## Changes made

1. Added a branch-vocabulary note documenting that legacy `negative_core` values in retained R02A/split files are equivalent to canonical `core_negative`.
2. Added an R02A/P02A equivalence note documenting that `P02A`/`p02a` prefixes refer to the same retained-assignment R02A hard-split stress test.
3. Corrected S2 R02A documentation file references to the current repository filenames.
4. Added standalone Figure 1 assets under `figures/`.
5. Included `.github/workflows/validate_repository.yml` in the regenerated package manifest and checksum inventory.
6. Regenerated `metadata/package_file_manifest.csv` and `metadata/SHA256SUMS.txt` after the patch.

## Items intentionally not changed

- R03/R04/R05/R06/R07 remain diagnostic/pilot-level provenance evidence.
- R08 remains attempted but non-interpreted.
- Frozen ESM-2 remains a controlled representation comparator, not a superior predictor.
- R02A remains a retained-assignment descriptive hard-split stress test, not definitive external validation.
- The core-negative n = 29 limitation remains visible.
- Sensitivity-negative peptides remain separate from the headline core-negative evaluation.
- Challenge-only sequences remain excluded from training, CV, hard-split headline evaluation, and tuning.

## Remaining author/institutional confirmations

- Final reviewer-access status, archival DOI, release date, and public license wording.
- Final author metadata, ORCID records, competing-interest confirmation, and related manuscript disclosure if required by the target journal.
