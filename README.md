# iDAOP: Antioxidant Peptide Benchmarking Framework

This repository provides the manuscript-facing release candidate for:

**Antioxidant Peptide Benchmark Dataset and Formal Transparent Baseline Evaluation with a Controlled Frozen ESM-2 Stress Comparison**

**iDAOP is a benchmark and evaluation framework for antioxidant peptide prediction studies, not a new standalone predictor or web server.** The repository supports branch-aware dataset release, transparent AAC baseline evaluation, retained-assignment R02A descriptive stress testing, and a controlled frozen ESM-2 comparison.

It does not claim stable frozen ESM-2 superiority over transparent AAC baselines.

## Current release status

**Status:** Phase 2 filled draft / internal pre-submission release candidate.

This package now contains real source tables, split manifests, QC logs, environment versions, scripts, and retained-assignment R02A documentation. It is still not a final public release until author, DOI, licensing, and journal-specific availability statements are confirmed.

## License and reuse status

This private staging repository does not yet grant a public reuse license. Code, data, split manifests, embeddings, results, and supplementary materials remain under provisional pre-submission review until institutional, source-database, journal, DOI, and archival-release decisions are finalized. See `LICENSE` and `DATA_LICENSE.md`.

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
- `results/` -- Table 6 source table, paired statistics, PLM aggregate/per-fold metrics, sensitivity behavior, AAC R02A core-only outputs.
- `qc/` -- QC manifest and JSON evidence for embedding, split matching, classifier execution, and R02A addendum.
- `environment/` -- confirmed package versions and environment files.
- `scripts/` -- analysis and QC scripts used to trace PLM outputs and validate this repository draft.
- `supplementary/` -- supplementary material map and R02A retained-assignment documentation.
- `docs/` -- GitHub Pages draft landing page.

## Quick validation

```bash
python scripts/validate_repository.py
```

Expected output:

```text
VALIDATION_STATUS: PASS
```

## Remaining release blockers

- Select and confirm repository license(s) for code and data.
- Fill final authors, affiliation, ORCID, repository URL, and DOI in `CITATION.cff`.
- Confirm target journal data/code availability wording.
- Decide whether large binary embedding files should be hosted in GitHub, Zenodo, or both.
- Run final public-safety scrub before making the repository public.
