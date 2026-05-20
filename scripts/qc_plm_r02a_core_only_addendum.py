#!/usr/bin/env python3
"""QC for PLM R02A core-only addendum outputs."""
import argparse
import json
from pathlib import Path
import pandas as pd


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-root", default=".")
    args = ap.parse_args()
    root = Path(args.project_root)
    out_root = root / 'outputs/plm_r02a_core_only_addendum_1_0'
    metrics_path = out_root / 'plm_r02a_core_only_addendum_per_fold_metrics_1_0.csv'
    preds_path = out_root / 'plm_r02a_core_only_addendum_predictions_1_0.csv'
    agg_path = out_root / 'plm_r02a_core_only_addendum_aggregate_summary_1_0.csv'
    manifest_path = out_root / 'plm_r02a_core_only_addendum_split_manifest_1_0.csv'
    run_manifest_path = out_root / 'plm_r02a_core_only_addendum_run_manifest_1_0.json'
    qc_out = out_root / 'plm_r02a_core_only_addendum_output_qc_1_0.json'

    missing = [str(p) for p in [metrics_path, preds_path, agg_path, manifest_path, run_manifest_path] if not p.exists()]
    if missing:
        qc = {'status': 'FAIL', 'missing_files': missing}
        qc_out.write_text(json.dumps(qc, indent=2), encoding='utf-8')
        print(json.dumps(qc, indent=2))
        return 1

    metrics = pd.read_csv(metrics_path)
    preds = pd.read_csv(preds_path)
    agg = pd.read_csv(agg_path)
    manifest = pd.read_csv(manifest_path)

    errors = []
    warnings = []
    expected_models = {'ESM2_LR_L2', 'ESM2_LinearSVM'}
    expected_units = 4
    expected_metric_rows = expected_units * len(expected_models)

    if len(metrics) != expected_metric_rows:
        errors.append(f'Expected {expected_metric_rows} metric rows; observed {len(metrics)}')
    if set(metrics.get('model_id', [])) != expected_models:
        errors.append(f'Model IDs mismatch: {sorted(set(metrics.get("model_id", [])))}')
    if set(metrics.get('analysis_branch', [])) != {'core_only'}:
        errors.append('analysis_branch must be core_only only')
    if set(metrics.get('split_family', [])) != {'r02a_sequence_cluster_hard_split'}:
        errors.append('split_family must be r02a_sequence_cluster_hard_split only')
    if len(agg) != 2:
        errors.append(f'Expected 2 aggregate rows; observed {len(agg)}')
    if 'branch_normalized' in manifest.columns and (manifest['branch_normalized'] == 'negative_sensitivity').any():
        errors.append('negative_sensitivity appears in addendum split manifest')
    if 'branch_normalized' in manifest.columns and (manifest['branch_normalized'] == 'challenge_only').any():
        errors.append('challenge_only appears in addendum split manifest')
    if 'branch_normalized' in preds.columns and (preds['branch_normalized'] == 'negative_sensitivity').any():
        errors.append('negative_sensitivity appears in addendum predictions')
    if 'branch_normalized' in preds.columns and (preds['branch_normalized'] == 'challenge_only').any():
        errors.append('challenge_only appears in addendum predictions')

    # Pred rows should be exactly two models times total test rows from the addendum manifest.
    test_n = int((manifest['split_role'] == 'test').sum()) if 'split_role' in manifest.columns else None
    expected_pred_rows = test_n * len(expected_models) if test_n is not None else None
    if expected_pred_rows is not None and len(preds) != expected_pred_rows:
        errors.append(f'Expected {expected_pred_rows} prediction rows; observed {len(preds)}')

    qc = {
        'status': 'PASS' if not errors else 'FAIL',
        'errors': errors,
        'warnings': warnings,
        'metric_rows': int(len(metrics)),
        'prediction_rows': int(len(preds)),
        'aggregate_rows': int(len(agg)),
        'addendum_manifest_rows': int(len(manifest)),
        'test_rows_in_manifest': int(test_n) if test_n is not None else None,
        'model_counts': metrics['model_id'].value_counts().to_dict() if 'model_id' in metrics.columns else {},
        'split_family_counts': metrics['split_family'].value_counts().to_dict() if 'split_family' in metrics.columns else {},
        'analysis_branch_counts': metrics['analysis_branch'].value_counts().to_dict() if 'analysis_branch' in metrics.columns else {},
        'branch_counts_manifest': manifest['branch_normalized'].value_counts().to_dict() if 'branch_normalized' in manifest.columns else {},
        'claim_boundary': 'This addendum only fills missing R02A core-only PLM hard-split cells; integrate with AAC matched comparison before manuscript interpretation.',
    }
    qc_out.write_text(json.dumps(qc, indent=2), encoding='utf-8')
    print(json.dumps(qc, indent=2))
    print('WROTE:', qc_out)
    return 0 if qc['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
