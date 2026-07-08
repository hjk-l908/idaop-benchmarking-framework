# iDAOP GitHub author metadata sync v1 change log

Status: FOR_REVIEW_NOT_FINAL
Date: 2026-07-08

## Purpose

Synchronize GitHub-facing repository metadata with the manuscript author list after confirmation that the second author name should be written as `Yu-Jie Weng` and after the author-side decision not to list ORCID identifiers in the repository files.

## Files changed

- `CITATION.cff`
  - Replaced the generic contributor entry with the manuscript author list:
    1. Hui-Ju Kao
    2. Yu-Jie Weng
    3. Chia-Hung Chen
    4. Chen-Lin Yu
    5. Kai-Yao Huang
    6. Shun-Long Weng
  - No ORCID identifiers were added.
  - DOI and final public-release metadata remain intentionally omitted/pending.

- `README.md`
  - Updated release-status wording to state that `CITATION.cff` now lists manuscript author names without ORCID identifiers.
  - Replaced the outdated remaining-blocker item about filling final authors/ORCID with a safer statement: author names/order should be reviewed, ORCID identifiers are not listed, and final DOI/release metadata remain pending.

- `PUBLIC_RELEASE_CHECKLIST.md`
  - Updated author/citation checklist wording to reflect that author names are now present in `CITATION.cff`, ORCID identifiers are not listed, and DOI/release metadata remain pending.

- `docs/index.md`
  - Updated the citation section to reflect current `CITATION.cff` author-name status and pending DOI/release metadata.

- `metadata/package_file_manifest.csv`
  - Regenerated after metadata edits.

- `metadata/SHA256SUMS.txt`
  - Regenerated after metadata edits.

## Validation performed

- `python3 scripts/validate_repository.py` → `VALIDATION_STATUS: PASS`
- `sha256sum -c metadata/SHA256SUMS.txt` → all listed files OK
- Manifest size/hash consistency check → PASS
- `CITATION.cff` YAML parse check → PASS; six authors detected; second author is `Yu-Jie Weng`

## Boundaries preserved

- No scientific result tables were modified.
- No model outputs were modified.
- No sequence/data branch assignments were modified.
- No R08 metric file was added.
- DOI, final license, public GitHub release, and archival release remain pending.
- ORCID identifiers were not added.
