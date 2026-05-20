#!/usr/bin/env python3
"""Validate PLM embedding dry-run outputs after ESM-2 embedding extraction."""
from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path

import numpy as np


def read_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--embedding-npz", required=True)
    ap.add_argument("--embedding-index", required=True)
    ap.add_argument("--expected-n", type=int, required=True)
    ap.add_argument("--out", default="outputs/qc/plm_dry_run_embedding_qc_report_1_0.json")
    args = ap.parse_args()

    npz_path = Path(args.embedding_npz)
    index_path = Path(args.embedding_index)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    report = {"status": "PASS", "errors": [], "warnings": []}
    if not npz_path.exists():
        report["errors"].append(f"Missing embedding NPZ: {npz_path}")
    if not index_path.exists():
        report["errors"].append(f"Missing embedding index CSV: {index_path}")
    if report["errors"]:
        report["status"] = "FAIL"
        out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
        raise SystemExit("Embedding output validation failed: missing files")

    data = np.load(npz_path, allow_pickle=False)
    embeddings = data["embeddings"]
    sequence_ids = data["sequence_ids"].astype(str).tolist()
    index_rows = read_csv(index_path)
    index_ids = [r.get("sequence_id", "") for r in index_rows]

    report.update({
        "embedding_shape": list(embeddings.shape),
        "n_index_rows": len(index_rows),
        "expected_n": args.expected_n,
    })
    if embeddings.ndim != 2:
        report["errors"].append("Embeddings array is not 2-dimensional")
    if embeddings.shape[0] != args.expected_n:
        report["errors"].append(f"Embedding row count {embeddings.shape[0]} != expected_n {args.expected_n}")
    if len(index_rows) != embeddings.shape[0]:
        report["errors"].append("Embedding index row count does not match embedding matrix row count")
    if sequence_ids != index_ids:
        report["errors"].append("sequence_ids stored in NPZ do not match embedding index order")
    if not np.isfinite(embeddings).all():
        report["errors"].append("Embedding matrix contains NaN or infinite values")
    if embeddings.shape[1] < 10:
        report["warnings"].append("Embedding dimension looks unexpectedly small")

    if report["errors"]:
        report["status"] = "FAIL"
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    if report["status"] != "PASS":
        raise SystemExit("Embedding output validation failed")


if __name__ == "__main__":
    main()
