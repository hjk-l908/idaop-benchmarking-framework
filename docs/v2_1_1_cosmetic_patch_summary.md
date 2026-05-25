# v2.1.1 cosmetic repository patch summary

This patch addresses the remaining non-scientific cosmetic items identified after the v2.1 targeted closure verification. It does not alter manuscript numbers, Table 6, branch membership, split assignments, diagnostic evidence status, or PLM/AAC interpretation.

## Changes made

- Added a `figures/` entry to the top-level repository `README.md`.
- Converted the unchecked R02A public-release checklist in `supplementary/R02A_retained_assignment_documentation_1_0.md` into a completed-status note.
- Updated the matching R02A supplementary DOCX with the same completed-status note.
- Added `metadata/public_safety_scan_v2_1_1.txt`.
- Regenerated `metadata/package_file_manifest.csv` and `metadata/SHA256SUMS.txt` after the patch.

## Scientific boundaries intentionally unchanged

- AAC_reference + L2 Logistic Regression remains the primary transparent baseline.
- AAC_reference + Linear SVM remains the secondary comparator.
- Frozen ESM-2 remains a controlled representation comparator, not a superior predictor.
- R02A remains a retained-assignment descriptive hard-split stress test.
- R03/R04/R05/R06/R07 remain diagnostic/pilot-level provenance evidence only.
- R08 remains attempted but non-interpreted.
- Sensitivity-negative sequences remain separate from the headline core-negative branch.
- Challenge-only sequences remain excluded from training, cross-validation, tuning, and headline metrics.
