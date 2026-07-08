# iDAOP GitHub public-release license patch v1

## Purpose

Prepare the GitHub repository metadata for public visibility, GitHub release creation, and Zenodo DOI archiving.

## Files changed

- `LICENSE`
- `DATA_LICENSE.md`
- `CITATION.cff`
- `README.md`
- `PUBLIC_RELEASE_CHECKLIST.md`
- `docs/index.md`
- `SECURITY_AND_PRIVACY_NOTES.md`
- `metadata/public_safety_scan_v2_1.txt`
- `metadata/public_safety_scan_v2_1_1.txt`
- `metadata/public_safety_scan_diagnostic_merge_v1.txt`
- `metadata/repository_validation_report.txt`
- `metadata/repository_validation_report_diagnostic_merge_v1.txt`
- `metadata/package_file_manifest.csv`
- `metadata/SHA256SUMS.txt`

## License decisions recorded

- Code, command wrappers, validation scripts, and software-oriented configuration files: MIT License.
- Public-safe author-prepared benchmark materials, documentation, result summaries, diagnostic tables, QC reports, supplementary maps, and figure assets: CC BY 4.0.
- Third-party source databases, external records, source PDFs, validation PDFs, restricted source materials, and non-redistributed source records are not relicensed by this repository.

## Scientific boundaries preserved

- iDAOP remains a benchmark/evaluation framework, not a standalone predictor or web server.
- AAC_reference + L2 Logistic Regression remains the primary transparent baseline.
- AAC_reference + Linear SVM remains a secondary comparator.
- Frozen ESM-2 remains a controlled representation comparator and does not support a stable-superiority claim.
- R02A remains a retained-assignment descriptive stress test.
- R08 remains attempted but non-interpreted and is not included as a metric-evidence file.
- Sensitivity-negative and challenge-only boundaries are unchanged.

## Remaining steps after applying this patch

1. Commit and push the patch to `main`.
2. Change repository visibility from private to public.
3. Create GitHub release `v1.0.0`.
4. Archive the release through Zenodo and obtain DOI.
5. Add DOI/release-date metadata to `CITATION.cff`, `README.md`, manuscript data availability, cover letter, and the final BIB submission package.
