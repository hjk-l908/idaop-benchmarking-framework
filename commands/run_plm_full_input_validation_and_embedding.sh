#!/usr/bin/env bash
set -euo pipefail

# Portable repository-root detection.
# Run this script from anywhere inside the cloned repository.
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

mkdir -p inputs/full_embedding outputs/embeddings outputs/qc logs

echo "[1/3] Validate full input CSV / FASTA / order manifest"
python3 scripts/validate_dry_run_inputs.py \
  --csv inputs/full_embedding/plm_full_embedding_input_for_esm2_1_0.csv \
  --fasta inputs/full_embedding/plm_full_embedding_input_for_esm2_1_0.fasta \
  --order inputs/full_embedding/plm_full_embedding_sequence_order_manifest_1_0.csv \
  2>&1 | tee logs/plm_full_input_validation_1_0.log

echo "[2/3] Run full ESM-2 embedding generation"
python3 scripts/run_esm2_embeddings.py \
  --config configs/plm_full_embedding_config_1_0.yaml \
  --generate \
  2>&1 | tee logs/plm_full_embedding_generation_1_0.log

echo "[3/3] Reminder: do not train classifiers until full embedding QC PASS is confirmed."
