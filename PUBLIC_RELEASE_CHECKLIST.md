# Public release checklist

This checklist records the public GitHub release, licensing, and Zenodo archival status for the iDAOP repository.

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

## Completed release actions

- [x] Change repository visibility from private to public after final user confirmation.
- [x] Create GitHub release `v1.0.1` for initial Zenodo archival DOI generation.
- [x] Archive GitHub release `v1.0.1` through Zenodo: https://doi.org/10.5281/zenodo.21254963.
- [x] Prepare citation metadata correction for a subsequent `v1.0.3` Zenodo archival release after revised Figure 1 synchronization.
- [ ] Confirm whether large binary embedding files should remain in GitHub, Zenodo, or both.
- [x] Re-run final repository validation and checksum verification after DOI metadata is added.


## Release citation

- GitHub release: `v1.0.3` (https://github.com/hjk-l908/idaop-benchmarking-framework/releases/tag/v1.0.3)
- Zenodo DOI: to be assigned by Zenodo for this release snapshot
- Release date: 2026-07-08
