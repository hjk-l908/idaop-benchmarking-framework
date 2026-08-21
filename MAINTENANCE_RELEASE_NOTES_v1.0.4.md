# iDAOP maintenance release notes v1.0.4

Initial maintenance candidate prepared: 2026-07-27
Independent audit reconciliation prepared: 2026-08-05
Paired-inference correction prepared: 2026-08-10
Release date: 2026-08-21

## Scope

This v1.0.4 maintenance release preserves the scientific datasets, branch assignments, split manifests, model predictions, Table 6 point estimates, and interpretation boundaries of archived release v1.0.3. It does not rerun a model, relabel a sequence, regenerate a split, or change branch membership. It does correct one statistical-reporting issue identified during author verification: random-CV paired inference is recomputed using the 10 sampling replicates as the inferential unit after averaging the four folds within each replicate, rather than treating 40 nested folds as independent pairs.

## Maintenance changes

- Establish and verify LF line-ending policy with `.gitattributes` so Git/GitHub source archives preserve the release text-byte convention.
- Regenerate `metadata/package_file_manifest.csv` and `metadata/SHA256SUMS.txt` from the actual release bytes.
- Add `scripts/verify_package_checksums.py` and include checksum verification in the GitHub Actions validation workflow.
- Harden checksum verification to detect malformed inventory lines, missing or modified listed files, and repository files omitted from the inventory.
- Replace stale current-status statements that said the v1.0.3 Zenodo DOI was still pending.
- Update the reviewer-facing supplementary-material map to reflect the retained-assignment R02A limitation and current public archive status.
- Add a maintenance change manifest covering all maintenance files changed relative to v1.0.3.
- Correct `results/paired_stats.csv` so random-CV paired tests use 10 replicate-level pairs. The LR_L2 core-only MCC delta remains +0.059, with corrected two-sided Wilcoxon p = 0.064 and bootstrap 95% CI +0.006 to +0.109; the sensitivity-augmented LR_L2 MCC delta remains +0.040, with p = 0.232 and CI -0.020 to +0.100.
- Preserve R02A as descriptive-only (n = 4) and preserve all Table 6 point estimates. The archived v1.0.3 `results/paired_stats.csv` remains the historical fold-level provenance record.

## Release boundary

The previous archived public release is v1.0.3 at https://doi.org/10.5281/zenodo.21270655. This v1.0.4 maintenance release is dated 2026-08-21. The version-specific v1.0.4 Zenodo DOI will be inserted only after it is actually assigned by Zenodo; it must not be guessed.
