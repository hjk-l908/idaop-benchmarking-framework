# QC evidence

`qc_manifest.csv` summarizes QC status and points to detailed JSON files.

Important QC boundaries:

- Full frozen ESM-2 embedding output passed shape/finite-value/order checks.
- Split matching passed no-missing-embedding and no-train/test-overlap checks.
- Challenge-only rows are absent from train/test manifests.
- R02A core-only addendum was derived by excluding negative_sensitivity rows from the retained R02A sensplus split.
- Original R02A cluster-generation command/script was not recovered and is documented as a limitation.
