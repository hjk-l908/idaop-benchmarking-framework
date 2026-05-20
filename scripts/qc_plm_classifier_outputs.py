#!/usr/bin/env python3
"""QC for PLM classifier full execution outputs."""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", default="outputs/plm_classifier_full_execution_1_0")
    ap.add_argument("--expected-metric-rows", type=int, default=168)
    args = ap.parse_args()

    root = Path(".").resolve()
    out = root / args.output_root
    metrics_path = out / "plm_classifier_full_per_fold_metrics_1_0.csv"
    pred_path = out / "plm_classifier_full_predictions_1_0.csv"
    agg_path = out / "plm_classifier_full_aggregate_summary_1_0.csv"
    sens_path = out / "plm_classifier_full_sensitivity_behavior_1_0.csv"
    qc_path = out / "plm_classifier_full_output_qc_1_0.json"

    errors = []
    warnings = []
    for p in [metrics_path, pred_path, agg_path, sens_path]:
        if not p.exists():
            errors.append(f"Missing output: {p}")

    if errors:
        qc = {"status": "FAIL", "errors": errors, "warnings": warnings}
        qc_path.parent.mkdir(parents=True, exist_ok=True)
        qc_path.write_text(json.dumps(qc, indent=2), encoding="utf-8")
        print(json.dumps(qc, indent=2))
        return 1

    m = pd.read_csv(metrics_path)
    p = pd.read_csv(pred_path)
    a = pd.read_csv(agg_path)
    s = pd.read_csv(sens_path)

    metric_cols = ["mcc", "auroc", "auprc", "f1", "precision", "sensitivity", "specificity"]
    if len(m) != args.expected_metric_rows:
        warnings.append(f"Metric row count is {len(m)}, expected {args.expected_metric_rows}")
    if m["run_id"].duplicated().any():
        errors.append("Duplicate run_id in per-fold metrics")
    for col in metric_cols:
        if col not in m.columns:
            errors.append(f"Missing metric column: {col}")
        elif m[col].isna().any():
            warnings.append(f"NaN values in metric column: {col}")
        elif not np.isfinite(m[col].astype(float)).all():
            errors.append(f"Non-finite values in metric column: {col}")

    if (p["branch"].astype(str) == "challenge_only").any() or (p.get("branch_normalized", "") == "challenge_only").any():
        errors.append("challenge_only found in classifier predictions")
    if not set(p["y_pred"].unique()).issubset({0, 1}):
        errors.append("y_pred contains non-binary values")
    if not set(p["y_true"].unique()).issubset({0, 1}):
        errors.append("y_true contains non-binary values")

    qc = {
        "status": "PASS" if not errors else "FAIL",
        "metrics_rows": int(len(m)),
        "prediction_rows": int(len(p)),
        "aggregate_rows": int(len(a)),
        "sensitivity_rows": int(len(s)),
        "model_counts": m["model_id"].value_counts().to_dict() if "model_id" in m else {},
        "split_family_counts": m["split_family"].value_counts().to_dict() if "split_family" in m else {},
        "analysis_branch_counts": m["analysis_branch"].value_counts().to_dict() if "analysis_branch" in m else {},
        "errors": errors,
        "warnings": warnings,
        "classifier_training_performed": True,
        "metrics_computed": True,
        "claim_boundary": "Interpret only after reviewing full output QC and matched AAC comparison.",
    }
    qc_path.write_text(json.dumps(qc, indent=2), encoding="utf-8")
    print(json.dumps(qc, indent=2))
    print("WROTE:", qc_path)
    return 0 if qc["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
