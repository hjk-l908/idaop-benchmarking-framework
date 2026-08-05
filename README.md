# iDAOP: Antioxidant Peptide Benchmarking Framework

This repository provides the manuscript-facing release candidate for:

**Antioxidant Peptide Benchmark Dataset and Formal Transparent Baseline Evaluation with a Controlled Frozen ESM-2 Stress Comparison**

**iDAOP is a benchmark and evaluation framework for antioxidant peptide prediction studies, not a new standalone predictor or web server.** The repository supports branch-aware dataset release, transparent AAC baseline evaluation, retained-assignment R02A descriptive stress testing, and a controlled frozen ESM-2 comparison.

It does not claim stable frozen ESM-2 superiority over transparent AAC baselines.

## Current release status

**Status:** Maintenance release candidate `v1.0.4-rc1`, prepared from the archived `v1.0.3` snapshot to correct archive-byte checksum consistency and stale release metadata.

The currently archived public release remains GitHub release `v1.0.3` with Zenodo DOI https://doi.org/10.5281/zenodo.21270655. This candidate has not yet been published or assigned a v1.0.4 DOI.

This package contains source tables, split manifests, QC logs, environment versions, scripts, retained-assignment R02A documentation, diagnostic traceability files, standalone Figure 1 assets, and a candidate-byte checksum inventory covering every repository file except the inventory file itself.

## License and reuse status

- Code, command wrappers, validation scripts, and software-oriented configuration files are released under the MIT License. See `LICENSE`.
- Public-safe author-prepared benchmark materials, documentation, result summaries, diagnostic tables, QC reports, supplementary maps, and figure assets are released under CC BY 4.0 unless otherwise stated. See `DATA_LICENSE.md`.
- These licenses do not grant rights over third-party source databases, source PDFs, validation PDFs, restricted source materials, or external records not redistributed in this repository.

## Key branch policy

| Branch | n | Use |
|---|---:|---|
| `positive_core` | 899 | positive branch for formal matched comparison |
| `core_negative` | 29 | headline negative branch |
| `negative_sensitivity` | 3 | sensitivity-only; not merged into headline core branch |
| `challenge_only` | 28 | post hoc stress-test only; never training/CV/headline metrics |

The three sensitivity-flagged negatives are `VLDTDY`, `LKALPMH`, and `IQKVAGTW`. They remain separate from the core-negative branch.

## Primary manuscript interpretation

The primary transparent baseline is AAC_reference + L2 Logistic Regression, with AAC_reference + Linear SVM as a secondary comparator. Frozen ESM-2 embeddings were used as a controlled stress comparison with matched LR/SVM classifiers. Results show setting-dependent random-CV gains for frozen ESM-2, but no stable hard-split superiority over AAC_reference. PLM gains often trade sensitivity for lower specificity.

## R02A status

R02A is retained as a **retained-assignment sequence-cluster hard-split stress test**. The retained assignment records the rule:

```text
exact + provided same-length identity80 + substring-containment connected components
```

The original cluster-generation command/script was not recovered. Therefore, R02A is reported as descriptive stress-test evidence only, not a fully regenerable clustering protocol. See `supplementary/R02A_retained_assignment_documentation_1_0.md`.

## Repository map

- `data/` -- branch manifest, full embedding input manifest, sequence order and branch summaries.
- `splits/` -- random-CV manifests, retained R02A assignment, R02A sensplus and core-only manifests.
- `results/` -- Table 6 source table, paired statistics, PLM aggregate/per-fold metrics, sensitivity behavior, AAC R02A core-only outputs, and diagnostic/pilot-level traditional-baseline traceability files in `results/diagnostic/`.
- `qc/` -- QC manifest and JSON evidence for embedding, split matching, classifier execution, and R02A addendum.
- `environment/` -- confirmed package versions and environment files.
- `figures/` -- standalone Figure 1 assets for submission.
- `scripts/` -- analysis and QC scripts used to trace PLM outputs and validate this repository snapshot.
- `supplementary/` -- supplementary material map and R02A retained-assignment documentation.
- `docs/` -- GitHub Pages draft landing page.
- `metadata/` -- candidate-byte manifest, SHA-256 inventory, validation summaries, and maintenance change manifest.

## Diagnostic traceability files

`results/diagnostic/` contains public-safe R01/R03/R04/R05/R06/R07 diagnostic CSV summaries used to restore reviewer-facing traceability for staged traditional-baseline and feature-family checks. These files are diagnostic/pilot-level provenance only; they do not replace the primary AAC_reference + L2 Logistic Regression baseline, do not promote AAC_plus_physchem or CKSAAP_k1 to main evidence, and do not support any claim of stable frozen ESM-2 superiority. R08 hard-split CKSAAP produced no usable public metric output and is intentionally not included or interpreted.

## Quick validation

```bash
python scripts/validate_repository.py
python scripts/verify_package_checksums.py
```

Expected output:

```text
VALIDATION_STATUS: PASS
CHECKSUM_STATUS: PASS
```

## Final archival tasks for v1.0.4

- Review this maintenance candidate and confirm that no additional repository changes are required.
- Commit the candidate with LF line endings preserved by `.gitattributes`.
- Create GitHub release `v1.0.4`.
- Archive the release through Zenodo and obtain the version-specific v1.0.4 DOI.
- Before tagging, convert `CITATION.cff` from `1.0.4-rc1` to final `1.0.4` metadata and add the release date; add the actual DOI to current-facing metadata only after Zenodo assigns it.
- Regenerate the manifest/checksum inventory after any final metadata edit, then extract each downloaded release archive and run `python scripts/verify_package_checksums.py` inside the extracted tree.

## Release and citation metadata

- GitHub repository: https://github.com/hjk-l908/idaop-benchmarking-framework
- Current archived GitHub release: `v1.0.3` (https://github.com/hjk-l908/idaop-benchmarking-framework/releases/tag/v1.0.3)
- Current archived Zenodo DOI: https://doi.org/10.5281/zenodo.21270655
- Maintenance candidate: `v1.0.4-rc1`
- Candidate prepared: 2026-07-27
- v1.0.4 DOI and release date: not yet assigned
- Code license: MIT License
- Public-safe benchmark materials and documentation: CC BY 4.0, as described in `DATA_LICENSE.md`
- ORCID identifiers are not listed in this repository snapshot per current author-side decision.

## Post-release maintenance notes

- Do not add source PDFs, validation PDFs, restricted source archives, raw FASTA/FA source files, credentials, API tokens, or private execution paths to future public releases.
- If additional files are added after this candidate, re-run repository validation, checksum verification, and public-safety review before minting a new archived release.
- Large binary embedding-file hosting decisions for future releases should be documented before any new archival release.
