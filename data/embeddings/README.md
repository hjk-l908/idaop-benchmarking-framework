# Embedding files

This folder includes the frozen ESM-2 embedding matrix and matching row index used for PLM classifier comparisons.

- `plm_full_esm2_embeddings_1_0.npz`: 959 x 1280 float32 frozen ESM-2 embeddings.
- `plm_full_esm2_embedding_index_1_0.csv`: sequence_id to embedding-row mapping.

Embedding configuration is documented in `configs/plm_full_embedding_config_1_0.yaml` and `environment/ENVIRONMENT_VERSIONS.md`.
