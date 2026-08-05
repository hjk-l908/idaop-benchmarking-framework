# iDAOP maintenance release notes v1.0.4 (candidate v1.0.4-rc1)

Candidate prepared: 2026-07-27
Independent audit reconciliation prepared: 2026-08-05

## Scope

This maintenance release candidate preserves the scientific datasets, branch assignments, split manifests, model outputs, reported metrics, and interpretation boundaries of archived release v1.0.3. It does not add a new analysis, rerun a model, relabel a sequence, or alter a manuscript result.

## Maintenance changes

- Establish and verify LF line-ending policy with `.gitattributes` so Git/GitHub source archives preserve the candidate text-byte convention.
- Regenerate `metadata/package_file_manifest.csv` and `metadata/SHA256SUMS.txt` from the actual candidate bytes.
- Add `scripts/verify_package_checksums.py` and include checksum verification in the GitHub Actions validation workflow.
- Harden checksum verification to detect malformed inventory lines, missing or modified listed files, and repository files omitted from the inventory.
- Replace stale current-status statements that said the v1.0.3 Zenodo DOI was still pending.
- Update the reviewer-facing supplementary-material map to reflect the retained-assignment R02A limitation and current public archive status.
- Add a maintenance change manifest covering all candidate files changed relative to v1.0.3.

## Release boundary

The currently archived public release remains v1.0.3 at https://doi.org/10.5281/zenodo.21270655. This candidate is not a public release and has no v1.0.4 version-specific DOI yet. Before tagging, `CITATION.cff` must be converted from candidate to final v1.0.4 metadata. The final DOI should be inserted only after it is actually assigned by Zenodo; it must not be guessed.
