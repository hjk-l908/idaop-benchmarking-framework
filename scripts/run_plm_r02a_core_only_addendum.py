#!/usr/bin/env python3
"""PLM R02A core-only addendum execution 1.0.

Purpose:
Create and execute the missing R02A hard-split core-only PLM comparison
from the existing R02A sensplus split by excluding sensitivity negatives.

This script uses frozen ESM-2 embeddings and the previously validated split
manifest. It does not fine-tune, change branches, or use challenge-only rows.
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


def build_core_only_addendum_manifest(spl: pd.DataFrame, cfg: Dict) -> pd.DataFrame:
    src = cfg["addendum_source"]
    source_split_family = src.get("source_split_family", "r02a_sequence_cluster_hard_split")
    source_analysis_branch = src.get("source_analysis_branch", "sensplus")
    output_analysis_branch = src.get("output_analysis_branch", "core_only")

    required_cols = [
        "split_family", "analysis_branch", "replicate_id", "fold_id", "split_role",
        "record_id", "sequence", "label", "branch",
    ]
    missing = [c for c in required_cols if c not in spl.columns]
    if missing:
        raise ValueError(f"Split manifest missing required columns: {missing}")

    work = spl[(spl["split_family"] == source_split_family) & (spl["analysis_branch"] == source_analysis_branch)].copy()
    if work.empty:
        raise ValueError("No R02A sensplus rows found in source split manifest.")

    work["branch_normalized"] = work["branch"].map(BRANCH_MAP).fillna(work["branch"])
    before_n = len(work)
    removed = work[work["branch_normalized"] == "negative_sensitivity"].copy()
    work = work[work["branch_normalized"] != "negative_sensitivity"].copy()

    if (work["branch_normalized"] == "challenge_only").any():
        raise ValueError("challenge_only detected in R02A core-only addendum manifest.")

    work["source_analysis_branch"] = work["analysis_branch"]
    work["analysis_branch"] = output_analysis_branch
    work["addendum_id"] = cfg["addendum_id"]
    work["addendum_note"] = "derived_from_r02a_sensplus_by_excluding_negative_sensitivity"

    # Preserve row order but make deterministic.
    sort_cols = ["split_family", "analysis_branch", "replicate_id", "fold_id", "split_role", "record_id"]
    work = work.sort_values(sort_cols).reset_index(drop=True)

    work.attrs["source_rows"] = before_n
    work.attrs["removed_sensitivity_rows"] = int(len(removed))
    work.attrs["output_rows"] = int(len(work))
    return work


def validate_manifest(add: pd.DataFrame, idx: pd.DataFrame, X: np.ndarray, cfg: Dict) -> Tuple[List[str], List[Dict]]:
    errors = []
    bad_units = []
    expected_dim = int(cfg["features"].get("expected_embedding_dim", 1280))
    if X.shape[0] != len(idx):
        errors.append(f"Embedding row mismatch: X={X.shape[0]} index={len(idx)}")
    if X.shape[1] != expected_dim:
        errors.append(f"Embedding dim mismatch: X={X.shape[1]} expected={expected_dim}")
    if not np.isfinite(X).all():
        errors.append("Embedding matrix contains NaN or Inf")
    if not idx["sequence_id"].is_unique:
        errors.append("Embedding index sequence_id is not unique")
    if (add["branch_normalized"] == "challenge_only").any():
        errors.append("challenge_only appears in addendum train/test manifest")
    if (add["branch_normalized"] == "negative_sensitivity").any():
        errors.append("negative_sensitivity appears in core-only addendum manifest")

    unit_cols = ["split_family", "analysis_branch", "replicate_id", "fold_id"]
    for key, g in add.groupby(unit_cols):
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
    return errors, bad_units


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
    out_root.mkdir(parents=True, exist_ok=True)

    add_manifest_path = out_root / cfg["outputs"]["addendum_split_manifest_csv"]
    metrics_path = out_root / cfg["outputs"]["per_fold_metrics_csv"]
    pred_path = out_root / cfg["outputs"]["predictions_csv"]
    agg_path = out_root / cfg["outputs"]["aggregate_summary_csv"]
    qc_path = out_root / cfg["outputs"]["qc_json"]
    manifest_path = out_root / cfg["outputs"]["run_manifest_json"]

    idx = pd.read_csv(emb_idx)
    spl = pd.read_csv(split_path)
    npz = np.load(emb_npz)
    array_key = "embeddings" if "embeddings" in npz.files else npz.files[0]
    X = npz[array_key]

    idx["branch_normalized"] = idx["branch"].map(BRANCH_MAP).fillna(idx["branch"])
    add = build_core_only_addendum_manifest(spl, cfg)
    id_to_row = {sid: i for i, sid in enumerate(idx["sequence_id"].astype(str))}
    add["embedding_row"] = add["record_id"].astype(str).map(id_to_row)

    errors = []
    missing_rows = int(add["embedding_row"].isna().sum())
    if missing_rows:
        errors.append(f"Missing embedding rows for addendum records: {missing_rows}")
    more_errors, bad_units = validate_manifest(add, idx, X, cfg)
    errors.extend(more_errors)

    add.to_csv(add_manifest_path, index=False)

    run_manifest = {
        "status": "PASS" if not errors and not bad_units else "FAIL",
        "addendum_id": cfg["addendum_id"],
        "config": str(cfg_path),
        "embedding_npz": str(emb_npz),
        "embedding_index": str(emb_idx),
        "source_split_manifest": str(split_path),
        "addendum_split_manifest": str(add_manifest_path),
        "array_key": array_key,
        "embedding_shape": list(X.shape),
        "source_r02a_sensplus_rows": int(add.attrs.get("source_rows", 0)),
        "removed_sensitivity_rows": int(add.attrs.get("removed_sensitivity_rows", 0)),
        "addendum_manifest_rows": int(len(add)),
        "split_units": int(add.groupby(["split_family", "analysis_branch", "replicate_id", "fold_id"]).ngroups),
        "branch_counts": add["branch_normalized"].value_counts().to_dict(),
        "role_counts": add["split_role"].value_counts().to_dict(),
        "label_counts": add["label"].value_counts().to_dict(),
        "models": cfg["models"],
        "errors": errors,
        "bad_units": bad_units[:100],
        "preflight_only": bool(args.preflight_only),
        "classifier_training_performed": False,
        "metrics_computed": False,
        "claim_boundary": "R02A core-only addendum fills missing PLM hard-split core-only comparison; interpret only after QC and integration with Table 6.",
    }

    if args.preflight_only or run_manifest["status"] != "PASS":
        manifest_path.write_text(json.dumps(run_manifest, indent=2), encoding="utf-8")
        qc_path.write_text(json.dumps(run_manifest, indent=2), encoding="utf-8")
        print(json.dumps(run_manifest, indent=2))
        return 0 if run_manifest["status"] == "PASS" else 1

    metrics_rows = []
    pred_frames = []
    unit_cols = ["split_family", "analysis_branch", "replicate_id", "fold_id"]
    units = list(add.groupby(unit_cols))

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

            run_id = f"PLM_R02A_COREONLY_ADDENDUM_{model_id}_{replicate_id}_fold{fold_id}"
            row = {
                "run_id": run_id,
                "addendum_id": cfg["addendum_id"],
                "feature": cfg["features"]["feature_name"],
                "model_id": model_id,
                "model_family": model_cfg["model_family"],
                "split_family": split_family,
                "analysis_branch": analysis_branch,
                "source_analysis_branch": cfg["addendum_source"]["source_analysis_branch"],
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
                "split_family", "analysis_branch", "source_analysis_branch", "replicate_id", "fold_id",
                "record_id", "sequence", "label", "branch", "branch_normalized"
            ]].copy()
            p["run_id"] = run_id
            p["addendum_id"] = cfg["addendum_id"]
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

    metrics_df.to_csv(metrics_path, index=False)
    pred_df.to_csv(pred_path, index=False)
    agg_df.to_csv(agg_path, index=False)

    run_manifest.update({
        "status": "PASS",
        "classifier_training_performed": True,
        "metrics_computed": True,
        "per_fold_metrics_csv": str(metrics_path),
        "predictions_csv": str(pred_path),
        "aggregate_summary_csv": str(agg_path),
        "n_metric_rows": int(len(metrics_df)),
        "n_prediction_rows": int(len(pred_df)),
        "n_aggregate_rows": int(len(agg_df)),
    })
    manifest_path.write_text(json.dumps(run_manifest, indent=2), encoding="utf-8")
    qc_path.write_text(json.dumps(run_manifest, indent=2), encoding="utf-8")

    print(json.dumps(run_manifest, indent=2))
    print("WROTE:", add_manifest_path)
    print("WROTE:", metrics_path)
    print("WROTE:", pred_path)
    print("WROTE:", agg_path)
    print("WROTE:", qc_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
