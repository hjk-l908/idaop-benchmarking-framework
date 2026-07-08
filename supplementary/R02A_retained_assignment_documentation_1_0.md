# R02A Retained-Assignment Documentation 1.0

**Antioxidant peptide benchmark manuscript - sequence-cluster hard-split stress test documentation**  
Prepared for manuscript, supplementary materials, and GitHub repository release.

## 1. Executive decision

**Decision:** R02A should be retained as a retained-assignment sequence-cluster hard-split stress test. It should not be replaced by a newly generated CD-HIT 80% split at this stage.

**Reason:** The original cluster-generation command or script was not recovered after project and home-directory searches. The retained assignment file preserves the split rule and cluster/fold assignments, and all downstream AAC and PLM R02A analyses used the same retained assignment. Therefore, R02A remains suitable as descriptive stress-test evidence but should not be described as a fully regenerable clustering protocol.

| Item | Documentation decision |
|---|---|
| R02A status | Retained-assignment sequence-cluster hard-split stress test |
| Original generation command/script | Not recovered |
| External tool claim | Do not claim CD-HIT, MMseqs2, BLAST, DIAMOND, or other external tool use unless later evidence is found |
| Current manuscript role | Descriptive hard-split stress-test evidence only |
| Replacement by new CD-HIT 80% split | Not recommended; would constitute a new hard-split protocol and require rerunning hard-split analyses |

## 2. Evidence basis and retained files

Primary retained source file:

```text
splits/PILOT_R02A_sequence_cluster_hard_split_assignments.csv
```

Downstream R02A source assignment and train/test manifests:

```text
splits/r02a_hard_split_source_assignments_1_0.csv
splits/r02a_hard_split_sensplus_manifest.csv
splits/r02a_hard_split_core_only_manifest.csv
splits/r02a_hard_split_manifest.csv
```

Terminology note: `R02A` is the manuscript-facing stage name. Legacy `P02A`/`p02a` prefixes used in filenames or column names refer to the same retained-assignment sequence-cluster hard-split stress test.

| File | Rows x columns | SHA256 |
|---|---:|---|
| splits/PILOT_R02A_sequence_cluster_hard_split_assignments.csv | 177 x 27 | a74707d1ddbf8cc847d9587112ffffcc0052234abe4e2695a65b3621c21d4ef1 |
| splits/r02a_hard_split_source_assignments_1_0.csv | 177 x 17 | d0ccb6e96e3e2462e60ddc78830e5001e8fff1da67c6506a28f99d61d81bda94 |
| splits/r02a_hard_split_sensplus_manifest.csv | 708 x 13 | f033f06584aa3feec98395f93b3f8daf6182ff1c5b80e22c6d3620f9735f3bb0 |
| splits/r02a_hard_split_core_only_manifest.csv | 696 x 19 | 5091e959a3fa66319f19a65fc666b3d6dcfe63d407cb8c0f293f28ff2924f3d0 |
| splits/r02a_hard_split_manifest.csv | 1404 x 20 | ac71d2156105a3dfb8bd477b9aecc3dd792a1d62d70d366eeaf0e23e0a0966b8 |

## 3. Retained R02A assignment summary

| Metric | Value |
|---|---:|
| Total retained assignment rows | 177 |
| Positive core rows | 145 |
| Core negative rows | 29 |
| Sensitivity-negative rows | 3 |
| Positive label rows | 145 |
| Negative label rows | 32 |
| R02A fold units | 4 |
| Unique P02A cluster IDs | 155 |
| Mixed-label clusters | 2 |
| Non-mixed-label clusters | 153 |

## 4. Recorded split rule

The retained assignment file records the following split rule exactly:

```text
exact + provided same-length identity80 + substring-containment connected components
```

Operational interpretation: sequences were assigned into connected components based on retained grouping information that combined exact sequence groups, same-length identity-80 relationships, and substring-containment relationships. These retained connected components were assigned to R02A hard-split folds. Train sets were defined as all non-test clusters/folds.

## 5. Fold and branch composition

|   p02a_hard_fold |   negative_core |   negative_sensitivity |   positive_core |
|-----------------:|----------------:|-----------------------:|----------------:|
|                1 |               7 |                      1 |              37 |
|                2 |               7 |                      1 |              36 |
|                3 |               8 |                      0 |              36 |
|                4 |               7 |                      1 |              36 |

Interpretation note: the core-only hard-split analysis excludes sensitivity-negative rows, whereas the sensplus analysis includes them as sensitivity cases. Challenge-only sequences must remain excluded from training, cross-validation, thresholding, and headline metrics.

Legacy `negative_core` branch-label note: some retained R02A/split files use `negative_core` to denote the same branch that the public data dictionary names `core_negative`. This is a legacy naming synonym only; no relabeling or branch reassignment is implied.

## 6. What should not be claimed

| Do not write | Use instead |
|---|---|
| R02A was generated using CD-HIT 80%. | R02A was implemented from a retained assignment file whose recorded rule included exact grouping, provided same-length identity-80 relationships, and substring-containment connected components. |
| R02A is a fully regenerable clustering protocol. | The retained assignment and downstream manifests are provided; the original cluster-generation command was not recovered. |
| R02A proves hard-split generalization. | R02A provides descriptive hard-split stress-test evidence. |
| PLM is robustly superior under hard split. | Frozen ESM-2 did not establish stable hard-split superiority over AAC_reference under the retained R02A stress-test setting. |
| Sensitivity negatives were merged into the core headline branch. | Sensitivity negatives were preserved as separate sensitivity cases and excluded from core-only headline rows. |

## 7. Manuscript-safe wording

### Methods wording

```text
R02A was implemented as a retained sequence-cluster hard-split assignment. The retained assignment file recorded the split rule as exact-sequence grouping plus provided same-length identity-80 relationships and substring-containment connected components. For each R02A fold, test sets comprised the clusters assigned to that fold, whereas train sets comprised all non-test clusters/folds. The same retained assignment was used for matched AAC_reference and frozen ESM-2 comparisons.
```

### Results / Table caption wording

```text
R02A hard-split rows are reported as descriptive stress-test estimates. The core-only rows exclude sensitivity-negative cases, whereas the sensplus rows retain them as sensitivity cases. Because R02A contains four fold units with small per-fold negative test counts, these rows should not be interpreted as stable inferential estimates.
```

### Limitations wording

```text
The original command or script used to generate the R02A retained assignment was not recovered. We therefore provide the retained assignment file, downstream train/test manifests, and checksum records, and interpret R02A as a descriptive stress-test split rather than as a fully regenerable clustering protocol. This limitation does not affect the matched downstream use of R02A for AAC_reference and frozen ESM-2 comparisons, but it limits claims about the cluster-generation protocol itself.
```

### Reviewer-response wording

```text
We agree that R02A should not be overinterpreted as a fully regenerable clustering protocol. We now describe R02A as a retained-assignment sequence-cluster hard-split stress test, provide the retained assignment and downstream manifests, and explicitly state that the original cluster-generation command was not recovered. All R02A conclusions have been restricted to descriptive stress-test evidence.
```

## 8. Public-release status note

The R02A retained-assignment documentation has been reconciled for the v2.1.1 public-facing release candidate. The retained source filenames are current, SHA-256 records are provided in `metadata/SHA256SUMS.txt`, R02A is described as descriptive-only in manuscript-facing wording, no external clustering-tool claim is made without recovered evidence, challenge-only sequences remain absent from R02A train/test manifests, and sensitivity-negative rows remain separate from core-only rows.

A final public-safety scan should still be repeated after any future author-side release changes, DOI updates, licensing changes, or repository restructuring.

## 9. Final recommended conclusion

R02A should remain in the manuscript as a retained-assignment sequence-cluster hard-split stress test. Its retained rule and downstream manifests are sufficient for matched AAC/PLM descriptive comparison, but the unrecovered original generation command prevents a fully regenerable clustering-protocol claim. Do not rerun CD-HIT 80% to replace R02A at this stage; that would create a new split protocol and require rerunning hard-split analyses.
