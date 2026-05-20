#!/usr/bin/env python3
"""PLM classifier full execution 1.0.

Frozen ESM-2 embedding matched comparison only.
No fine-tuning, no branch redefinition, no challenge-only train/CV.
"""
import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import yaml
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    matthews_corrcoef,
    roc_auc_score,
    average_precision_score,
    f1_score,
    precision_score,
    recall_score,
    confusion_matrix,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC

BRANCH_MAP = {
    "positive": "positive_core",
    "positive_core": "positive_core",
    "core_negative": "core_negative",
    "negative_core": "core_negative",
    "sensitivity_negative": "negative_sensitivity",
    "negative_sensitivity": "negative_sensitivity",
    "challenge_only": "challenge_only",
}


def load_config(path: Path) -> Dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def resolve(root: Path, maybe_rel: str) -> Path:
    p = Path(maybe_rel)
    return p if p.is_absolute() else root / p


def build_model(model_cfg: Dict) -> Pipeline:
    family = model_cfg["model_family"]
    if family == "LogisticRegression":
        clf = LogisticRegression(
            penalty=model_cfg.get("penalty", "l2"),
            solver=model_cfg.get("solver", "liblinear"),
            class_weight=model_cfg.get("class_weight", "balanced"),
            max_iter=int(model_cfg.get("max_iter", 1000)),
            random_state=int(model_cfg.get("random_state", 42)),
        )
    elif family == "LinearSVM":
        clf = LinearSVC(
            C=float(model_cfg.get("C", 1.0)),
            class_weight=model_cfg.get("class_weight", "balanced"),
            max_iter=int(model_cfg.get("max_iter", 5000)),
            random_state=int(model_cfg.get("random_state", 42)),
        )
    else:
        raise ValueError(f"Unsupported model_family: {family}")
    return Pipeline([("scaler", StandardScaler()), ("clf", clf)])


def predict_scores(model: Pipeline, model_cfg: Dict, X_test: np.ndarray) -> Tuple[np.ndarray, np.ndarray, str]:
    family = model_cfg["model_family"]
    threshold = float(model_cfg.get("decision_threshold", 0.5 if family == "LogisticRegression" else 0.0))
    if family == "LogisticRegression":
        score = model.predict_proba(X_test)[:, 1]
        pred = (score >= threshold).astype(int)
        score_type = "prob_positive"
    else:
        score = model.decision_function(X_test)
        pred = (score >= threshold).astype(int)
        score_type = "decision_function"
    return score, pred, score_type


def safe_metric(fn, default=np.nan):
    try:
        return float(fn())
    except Exception:
        return float(default)


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray, y_score: np.ndarray) -> Dict:
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    specificity = tn / (tn + fp) if (tn + fp) else np.nan
    return {
        "mcc": float(matthews_corrcoef(y_true, y_pred)),
        "auroc": safe_metric(lambda: roc_auc_score(y_true, y_score)),
        "auprc": safe_metric(lambda: average_precision_score(y_true, y_score)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "sensitivity": float(recall_score(y_true, y_pred, zero_division=0)),
        "specificity": float(specificity),
        "tp": int(tp),
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
    }


def validate_inputs(idx: pd.DataFrame, spl: pd.DataFrame, X: np.ndarray, cfg: Dict) -> List[str]:
    errors = []
    expected_dim = int(cfg["features"].get("expected_embedding_dim", 1280))
    if X.shape[0] != len(idx):
        errors.append(f"Embedding row mismatch: X={X.shape[0]} index={len(idx)}")
    if X.shape[1] != expected_dim:
        errors.append(f"Embedding dim mismatch: X={X.shape[1]} expected={expected_dim}")
    if not np.isfinite(X).all():
        errors.append("Embedding matrix contains NaN or Inf")
    if not idx["sequence_id"].is_unique:
        errors.append("Embedding index sequence_id is not unique")
    if (spl["branch_normalized"] == "challenge_only").any():
        errors.append("challenge_only appears in train/test split manifest")
    allowed_roles = set(cfg["run_scope"].get("allowed_split_roles", ["train", "test"]))
    bad_roles = sorted(set(spl["split_role"].astype(str)) - allowed_roles)
    if bad_roles:
        errors.append(f"Unexpected split_role values: {bad_roles}")
    return errors


def aggregate_metrics(metrics_df: pd.DataFrame) -> pd.DataFrame:
    metric_cols = ["mcc", "auroc", "auprc", "f1", "precision", "sensitivity", "specificity"]
    groups = ["feature", "model_id", "split_family", "analysis_branch"]
    rows = []
    for key, g in metrics_df.groupby(groups, dropna=False):
        row = dict(zip(groups, key))
        row["n_units"] = int(len(g))
        for col in metric_cols:
            row[f"{col}_mean"] = float(g[col].mean())
            row[f"{col}_std"] = float(g[col].std(ddof=1)) if len(g) > 1 else np.nan
            row[f"{col}_median"] = float(g[col].median())
        row["train_n_mean"] = float(g["train_n"].mean())
        row["test_n_mean"] = float(g["test_n"].mean())
        rows.append(row)
    return pd.DataFrame(rows)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--preflight-only", action="store_true")
    args = ap.parse_args()

    cfg_path = Path(args.config)
    cfg = load_config(cfg_path)
    root = Path(cfg["project_root"])

    emb_npz = resolve(root, cfg["inputs"]["embedding_npz"])
    emb_idx = resolve(root, cfg["inputs"]["embedding_index_csv"])
    split_path = resolve(root, cfg["inputs"]["split_manifest_csv"])

    out_root = resolve(root, cfg["outputs"]["output_root"])
    metrics_path = out_root / cfg["outputs"]["per_fold_metrics_csv"]
    pred_path = out_root / cfg["outputs"]["predictions_csv"]
    agg_path = out_root / cfg["outputs"]["aggregate_summary_csv"]
    sens_path = out_root / cfg["outputs"]["sensitivity_behavior_csv"]
    qc_path = out_root / cfg["outputs"]["qc_json"]
    manifest_path = out_root / cfg["outputs"]["run_manifest_json"]
    out_root.mkdir(parents=True, exist_ok=True)

    idx = pd.read_csv(emb_idx)
    spl = pd.read_csv(split_path)
    npz = np.load(emb_npz)
    array_key = "embeddings" if "embeddings" in npz.files else npz.files[0]
    X = npz[array_key]

    idx["branch_normalized"] = idx["branch"].map(BRANCH_MAP).fillna(idx["branch"])
    spl["branch_normalized"] = spl["branch"].map(BRANCH_MAP).fillna(spl["branch"])
    id_to_row = {sid: i for i, sid in enumerate(idx["sequence_id"].astype(str))}
    spl["embedding_row"] = spl["record_id"].astype(str).map(id_to_row)

    errors = validate_inputs(idx, spl, X, cfg)
    missing_rows = int(spl["embedding_row"].isna().sum())
    if missing_rows:
        errors.append(f"Missing embedding rows for split records: {missing_rows}")

    split_families = set(cfg["run_scope"]["split_families"])
    analysis_branches = set(cfg["run_scope"]["analysis_branches"])
    spl = spl[spl["split_family"].isin(split_families) & spl["analysis_branch"].isin(analysis_branches)].copy()

    unit_cols = ["split_family", "analysis_branch", "replicate_id", "fold_id"]
    units = list(spl.groupby(unit_cols))
    bad_units = []
    for key, g in units:
        train = g[g["split_role"] == "train"]
        test = g[g["split_role"] == "test"]
        if train.empty or test.empty:
            bad_units.append({"unit": list(key), "reason": "missing train or test"})
            continue
        if train["label"].astype(int).nunique() < 2:
            bad_units.append({"unit": list(key), "reason": "train one class only"})
        if test["label"].astype(int).nunique() < 2:
            bad_units.append({"unit": list(key), "reason": "test one class only"})
        if set(train["record_id"].astype(str)) & set(test["record_id"].astype(str)):
            bad_units.append({"unit": list(key), "reason": "train/test overlap"})

    preflight_status = "PASS" if not errors and not bad_units else "FAIL"
    run_manifest = {
        "status": preflight_status,
        "config": str(cfg_path),
        "embedding_npz": str(emb_npz),
        "embedding_index": str(emb_idx),
        "split_manifest": str(split_path),
        "array_key": array_key,
        "embedding_shape": list(X.shape),
        "split_rows_after_scope_filter": int(len(spl)),
        "split_units": int(len(units)),
        "models": cfg["models"],
        "errors": errors,
        "bad_units": bad_units[:100],
        "preflight_only": bool(args.preflight_only),
        "classifier_training_performed": False,
        "metrics_computed": False,
        "claim_boundary": "Full metrics require QC pass before interpretation; no challenge-only training/CV.",
    }

    if args.preflight_only or preflight_status != "PASS":
        manifest_path.write_text(json.dumps(run_manifest, indent=2), encoding="utf-8")
        qc_path.write_text(json.dumps(run_manifest, indent=2), encoding="utf-8")
        print(json.dumps(run_manifest, indent=2))
        return 0 if preflight_status == "PASS" else 1

    metrics_rows = []
    pred_frames = []

    for model_cfg in cfg["models"]:
        model_id = model_cfg["model_id"]
        for key, g in units:
            split_family, analysis_branch, replicate_id, fold_id = key
            train = g[g["split_role"] == "train"].copy()
            test = g[g["split_role"] == "test"].copy()

            X_train = X[train["embedding_row"].astype(int).values]
            y_train = train["label"].astype(int).values
            X_test = X[test["embedding_row"].astype(int).values]
            y_test = test["label"].astype(int).values

            clf = build_model(model_cfg)
            clf.fit(X_train, y_train)
            score, pred, score_type = predict_scores(clf, model_cfg, X_test)
            m = compute_metrics(y_test, pred, score)

            run_id = f"PLM_{model_id}_{split_family}_{analysis_branch}_{replicate_id}_fold{fold_id}"
            row = {
                "run_id": run_id,
                "feature": cfg["features"]["feature_name"],
                "model_id": model_id,
                "model_family": model_cfg["model_family"],
                "split_family": split_family,
                "analysis_branch": analysis_branch,
                "replicate_id": replicate_id,
                "fold_id": fold_id,
                "threshold": float(model_cfg.get("decision_threshold", 0.5)),
                "train_n": int(len(train)),
                "test_n": int(len(test)),
                "train_pos": int((y_train == 1).sum()),
                "train_neg": int((y_train == 0).sum()),
                "test_pos": int((y_test == 1).sum()),
                "test_neg": int((y_test == 0).sum()),
            }
            row.update(m)
            metrics_rows.append(row)

            p = test[[
                "split_family", "analysis_branch", "replicate_id", "fold_id",
                "record_id", "sequence", "label", "branch", "branch_normalized"
            ]].copy()
            p["run_id"] = run_id
            p["feature"] = cfg["features"]["feature_name"]
            p["model_id"] = model_id
            p["model_family"] = model_cfg["model_family"]
            p["y_true"] = y_test
            p["y_pred"] = pred
            p["score_positive"] = score
            p["score_type"] = score_type
            pred_frames.append(p)

    metrics_df = pd.DataFrame(metrics_rows)
    pred_df = pd.concat(pred_frames, ignore_index=True)
    agg_df = aggregate_metrics(metrics_df)

    # Sensitivity behavior summary from test predictions only.
    sens_df = pred_df[pred_df["branch_normalized"] == "negative_sensitivity"].copy()
    if not sens_df.empty:
        sens_summary = sens_df.groupby(["record_id", "sequence", "model_id", "split_family", "analysis_branch"]).agg(
            n_tests=("record_id", "size"),
            n_pred_positive=("y_pred", "sum"),
            mean_score_positive=("score_positive", "mean"),
            median_score_positive=("score_positive", "median"),
        ).reset_index()
        sens_summary["pred_positive_rate"] = sens_summary["n_pred_positive"] / sens_summary["n_tests"]
    else:
        sens_summary = pd.DataFrame(columns=[
            "record_id", "sequence", "model_id", "split_family", "analysis_branch",
            "n_tests", "n_pred_positive", "mean_score_positive", "median_score_positive", "pred_positive_rate"
        ])

    metrics_df.to_csv(metrics_path, index=False)
    pred_df.to_csv(pred_path, index=False)
    agg_df.to_csv(agg_path, index=False)
    sens_summary.to_csv(sens_path, index=False)

    run_manifest.update({
        "status": "PASS",
        "classifier_training_performed": True,
        "metrics_computed": True,
        "per_fold_metrics_csv": str(metrics_path),
        "predictions_csv": str(pred_path),
        "aggregate_summary_csv": str(agg_path),
        "sensitivity_behavior_csv": str(sens_path),
        "n_metric_rows": int(len(metrics_df)),
        "n_prediction_rows": int(len(pred_df)),
        "n_aggregate_rows": int(len(agg_df)),
        "n_sensitivity_summary_rows": int(len(sens_summary)),
    })
    manifest_path.write_text(json.dumps(run_manifest, indent=2), encoding="utf-8")
    qc_path.write_text(json.dumps(run_manifest, indent=2), encoding="utf-8")

    print(json.dumps(run_manifest, indent=2))
    print("WROTE:", metrics_path)
    print("WROTE:", pred_path)
    print("WROTE:", agg_path)
    print("WROTE:", sens_path)
    print("WROTE:", qc_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
