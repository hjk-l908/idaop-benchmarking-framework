# iDAOP GitHub Zenodo CFF fix v1 change log

Date: 2026-07-08

Purpose: Correct GitHub citation metadata after Zenodo failed to archive release v1.0.2 with the error `Citation metadata load failed`.

Changes:
- Updated `CITATION.cff` for the next Zenodo-trigger release (`v1.0.3`).
- Removed the previously minted v1.0.1 DOI from `CITATION.cff` to avoid stale release metadata during Zenodo ingestion.
- Simplified the CFF license field to `MIT` while keeping the separate data/materials license documented in `DATA_LICENSE.md`.
- Retained all author names without ORCID identifiers.
- Updated selected public-facing repository status text to avoid stale v1.0.1 DOI language in the v1.0.3 archive.
- No scientific results, dataset branches, model roles, interpretation boundaries, diagnostic evidence status, or manuscript conclusions were changed.

Recommended next release:
- Create GitHub release `v1.0.3` after this patch is committed and pushed.
- Use the DOI newly assigned by Zenodo to `v1.0.3` for the final submission package.
