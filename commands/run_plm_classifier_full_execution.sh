#!/usr/bin/env bash
set -euo pipefail

# Portable repository-root detection.
# Run this script from anywhere inside the cloned repository.
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

mkdir -p logs

python3 scripts/run_plm_classifiers.py \
  --config configs/plm_classifier_full_execution_config_1_0.yaml \
  2>&1 | tee logs/plm_classifier_full_execution_1_0.log
