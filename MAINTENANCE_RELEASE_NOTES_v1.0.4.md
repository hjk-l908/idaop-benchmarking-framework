# iDAOP maintenance release notes v1.0.4

Candidate prepared: 2026-07-27

## Scope

This maintenance release candidate preserves the scientific datasets, branch assignments, split manifests, model outputs, reported metrics, and interpretation boundaries of archived release v1.0.3. It does not add a new analysis, rerun a model, relabel a sequence, or alter a manuscript result.

## Maintenance changes

- Normalize repository text files to LF line endings and add `.gitattributes` so Git/GitHub source archives preserve the same text-byte convention.
- Regenerate `metadata/package_file_manifest.csv` and `metadata/SHA256SUMS.txt` from the actual candidate bytes.
- Add `scripts/verify_package_checksums.py` and include checksum verification in the GitHub Actions validation workflow.
- Replace stale current-status statements that said the v1.0.3 Zenodo DOI was still pending.
- Update the reviewer-facing supplementary-material map to reflect that a public repository DOI exists.
- Add a maintenance change manifest for auditability.

## Release boundary

The currently archived public release remains v1.0.3 at https://doi.org/10.5281/zenodo.21270655. This candidate is not a public release and has no v1.0.4 version-specific DOI yet. A final release date and DOI should be inserted only after the candidate is committed, tagged, released on GitHub, and archived by Zenodo.
