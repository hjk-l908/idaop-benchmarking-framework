# GitHub release-readiness audit after diagnostic merge

## Summary

This patch merges the curated diagnostic traceability package into the GitHub repository at:

`results/diagnostic/`

The diagnostic folder contains public-safe R01/R03/R04/R05/R06/R07 CSV summaries plus a README. These files support supplementary provenance and reviewer-facing traceability for staged traditional-baseline and feature-family checks. They are diagnostic/pilot-level only and do not replace the primary AAC_reference + L2 Logistic Regression baseline.

## Placement

Correct placement:

```text
idaop-benchmarking-framework/
  results/
    diagnostic/
```

The diagnostic files should not be placed at the repository root and should not replace files in `supplementary/`.

## Scientific framing retained

- AAC_reference + L2 Logistic Regression remains the primary transparent baseline.
- AAC_reference + Linear SVM remains a secondary comparator.
- Frozen ESM-2 remains a controlled representation comparator.
- R02A remains a retained-assignment descriptive hard-split stress test.
- R03/R04/R05/R06/R07 remain diagnostic/pilot-level provenance only.
- R08 remains attempted but non-interpreted; no R08 metric output is included.
- Sensitivity-negative peptides remain separate from headline core-negative evaluation.
- Challenge-only sequences remain excluded from training, cross-validation, tuning, and headline metrics.

## Files synchronized

The release candidate includes synchronized documentation and inventory files:

- `README.md`
- `results/README.md`
- `results/diagnostic/README.md`
- `supplementary/supplementary_materials_map.md`
- `data/data_dictionary.csv`
- `splits/README.md`
- `metadata/package_file_manifest.csv`
- `metadata/SHA256SUMS.txt`

## Remaining author/institutional items

These are not repo-content errors and should remain pending until confirmed:

- Final public/reviewer-access status.
- Final data and code license wording.
- Archival DOI and release tag.
- Manuscript author metadata and ORCID details.

## Recommendation

Use this release candidate as the current GitHub working baseline. Do not push older repo snapshots that lack `results/diagnostic/` and `figures/`.
