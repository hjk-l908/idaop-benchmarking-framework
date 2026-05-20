#!/usr/bin/env bash
set -euo pipefail

# Portable repository-root detection.
# Run this script from anywhere inside the cloned repository.
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

mkdir -p logs

python3 scripts/run_plm_r02a_core_only_addendum.py \
  --config configs/plm_r02a_core_only_addendum_config_1_0.yaml \
  2>&1 | tee logs/plm_r02a_core_only_addendum_execution_1_0.log
