#!/usr/bin/env python3
"""
ESM-2 full-embedding support script 1.0

Purpose
-------
Preflight-validate full embedding CSV/FASTA inputs and, only when --generate is set,
run frozen ESM-2 embedding extraction. This script must not train classifiers or
compute manuscript metrics.

Expected package layout
-----------------------
configs/plm_full_embedding_config_1_0.yaml
data/full_embedding_input_for_esm2_1_0.csv
data/full_embedding_sequence_order_manifest_1_0.csv
inputs/full_embedding/plm_full_embedding_input_for_esm2_1_0.fasta
outputs/embeddings/
outputs/qc/
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

try:
    import yaml
except Exception as exc:  # pragma: no cover
    raise SystemExit("Missing dependency: pyyaml. Install with: pip install pyyaml") from exc

ALLOWED_DEFAULT = set("ACDEFGHIKLMNPQRSTVWY")


def read_fasta(path: Path) -> List[Tuple[str, str]]:
    records: List[Tuple[str, str]] = []
    current_id = None
    current_seq: List[str] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if current_id is not None:
                    records.append((current_id, "".join(current_seq).upper()))
                raw_id = line[1:].split()[0]
                # Dry-run FASTA headers may use: order|dry_run_id|sequence_id|label=...|branch=...
                parts = raw_id.split("|")
                current_id = parts[2] if len(parts) >= 3 else raw_id
                current_seq = []
            else:
                current_seq.append(line.strip())
    if current_id is not None:
        records.append((current_id, "".join(current_seq).upper()))
    return records


def read_csv_rows(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: List[Dict[str, object]], fieldnames: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def preflight(config: dict, package_root: Path) -> Tuple[dict, List[Dict[str, object]]]:
    ds = config["dataset"]
    qc_cfg = config.get("qc", {})
    allowed = set(qc_cfg.get("allowed_characters", "")) or ALLOWED_DEFAULT

    csv_path = package_root / ds["input_csv"]
    fasta_path = package_root / ds["input_fasta"]
    order_manifest_path = package_root / ds.get("sequence_order_manifest", "")
    id_col = ds.get("sequence_id_column", "sequence_id")
    seq_col = ds.get("sequence_column", "sequence")
    label_col = ds.get("label_column", "label")
    branch_col = ds.get("branch_column", "branch")
    expected_n = int(ds.get("expected_n_sequences", -1))

    rows = read_csv_rows(csv_path)
    fasta_records = read_fasta(fasta_path)
    fasta_map = {rid: seq for rid, seq in fasta_records}

    seen_ids = set()
    seen_seqs = set()
    order_rows: List[Dict[str, object]] = []
    errors: List[str] = []
    warnings: List[str] = []

    if expected_n >= 0 and len(rows) != expected_n:
        errors.append(f"CSV row count {len(rows)} != expected_n_sequences {expected_n}")
    if len(fasta_records) != len(rows):
        errors.append(f"FASTA record count {len(fasta_records)} != CSV row count {len(rows)}")

    for idx, row in enumerate(rows):
        sid = str(row.get(id_col, "")).strip()
        seq = str(row.get(seq_col, "")).strip().upper()
        label = str(row.get(label_col, "")).strip()
        branch = str(row.get(branch_col, "")).strip()
        invalid = sorted(set(seq) - allowed)
        duplicate_id = sid in seen_ids
        duplicate_seq = seq in seen_seqs
        fasta_seq = fasta_records[idx][1] if idx < len(fasta_records) else None
        fasta_id = fasta_records[idx][0] if idx < len(fasta_records) else None
        order_match = (sid == fasta_id and seq == fasta_seq)
        in_fasta_map = sid in fasta_map

        if not sid:
            errors.append(f"Row {idx}: missing sequence_id")
        if not seq:
            errors.append(f"Row {idx}: missing sequence")
        if invalid:
            errors.append(f"{sid}: invalid residues {invalid}")
        if duplicate_id and qc_cfg.get("fail_on_duplicate_sequence_id", True):
            errors.append(f"Duplicate sequence_id: {sid}")
        if duplicate_seq and qc_cfg.get("fail_on_duplicate_sequence", False):
            errors.append(f"Duplicate sequence: {sid}")
        if not in_fasta_map:
            errors.append(f"{sid}: sequence_id missing from FASTA")
        if not order_match and qc_cfg.get("preserve_input_order", True):
            errors.append(f"{sid}: CSV/FASTA order or sequence mismatch at row {idx}")
        elif not order_match:
            warnings.append(f"{sid}: CSV/FASTA order mismatch at row {idx}")

        order_rows.append({
            "row_index": idx,
            "sequence_id_csv": sid,
            "sequence_id_fasta": fasta_id if fasta_id is not None else "",
            "sequence_length": len(seq),
            "label": label,
            "branch": branch,
            "csv_fasta_order_match": order_match,
            "invalid_residue_count": len(invalid),
            "duplicate_sequence_id": duplicate_id,
            "duplicate_sequence": duplicate_seq,
            "status": "PASS" if order_match and not invalid and not duplicate_id else "CHECK",
        })
        seen_ids.add(sid)
        seen_seqs.add(seq)

    if order_manifest_path and order_manifest_path.exists():
        manifest_rows = read_csv_rows(order_manifest_path)
        if len(manifest_rows) != len(rows):
            warnings.append("Sequence order manifest row count differs from dry-run CSV row count")

    report = {
        "status": "PASS" if not errors else "FAIL",
        "n_csv_rows": len(rows),
        "n_fasta_records": len(fasta_records),
        "expected_n_sequences": expected_n,
        "n_errors": len(errors),
        "n_warnings": len(warnings),
        "errors": errors,
        "warnings": warnings,
        "message": "Preflight only; no embedding or classifier metrics computed.",
    }
    return report, order_rows


def load_esm_model(model_name: str):
    """Load a fair-esm checkpoint by simple registry name."""
    try:
        import torch
        import esm
    except Exception as exc:  # pragma: no cover
        raise SystemExit(
            "Missing PLM dependencies. Install in the PLM environment, for example: "
            "pip install torch fair-esm"
        ) from exc

    registry = {
        "esm2_t6_8M_UR50D": esm.pretrained.esm2_t6_8M_UR50D,
        "esm2_t12_35M_UR50D": esm.pretrained.esm2_t12_35M_UR50D,
        "esm2_t30_150M_UR50D": esm.pretrained.esm2_t30_150M_UR50D,
        "esm2_t33_650M_UR50D": esm.pretrained.esm2_t33_650M_UR50D,
    }
    if model_name not in registry:
        raise SystemExit(f"Unsupported model_name for this dry-run script: {model_name}")
    model, alphabet = registry[model_name]()
    return model, alphabet


def generate_embeddings(config: dict, package_root: Path) -> None:
    import numpy as np
    import torch

    ds = config["dataset"]
    model_cfg = config["model"]
    out_cfg = config["outputs"]

    csv_path = package_root / ds["input_csv"]
    id_col = ds.get("sequence_id_column", "sequence_id")
    seq_col = ds.get("sequence_column", "sequence")
    label_col = ds.get("label_column", "label")
    branch_col = ds.get("branch_column", "branch")
    rows = read_csv_rows(csv_path)

    model_name = model_cfg.get("checkpoint_candidate", "esm2_t33_650M_UR50D")
    repr_layer = int(model_cfg.get("repr_layer", 33))
    batch_size = int(model_cfg.get("batch_size", 2))
    device_setting = str(model_cfg.get("device", "auto"))
    device = "cuda" if device_setting == "auto" and torch.cuda.is_available() else ("cpu" if device_setting == "auto" else device_setting)

    model, alphabet = load_esm_model(model_name)
    model.eval()
    model = model.to(device)
    batch_converter = alphabet.get_batch_converter()

    labels = [(row[id_col], row[seq_col]) for row in rows]
    all_embeddings = []
    index_rows = []
    output_dir = package_root / out_cfg["output_dir"]
    output_dir.mkdir(parents=True, exist_ok=True)

    with torch.no_grad():
        for start in range(0, len(labels), batch_size):
            batch = labels[start:start + batch_size]
            batch_labels, batch_strs, batch_tokens = batch_converter(batch)
            batch_tokens = batch_tokens.to(device)
            results = model(batch_tokens, repr_layers=[repr_layer], return_contacts=False)
            token_representations = results["representations"][repr_layer]
            for i, (sid, seq) in enumerate(batch):
                # fair-esm tokens include BOS at index 0 and EOS after sequence.
                emb = token_representations[i, 1:len(seq)+1].mean(0).detach().cpu().numpy().astype("float32")
                all_embeddings.append(emb)
                original_row = rows[start + i]
                index_rows.append({
                    "embedding_row_index": start + i,
                    "sequence_id": sid,
                    "sequence_length": len(seq),
                    "label": original_row.get(label_col, ""),
                    "branch": original_row.get(branch_col, ""),
                    "model_name": model_name,
                    "repr_layer": repr_layer,
                    "pooling": "mean_non_special_tokens",
                })
    matrix = np.vstack(all_embeddings)
    npz_path = output_dir / out_cfg["embedding_npz"]
    np.savez_compressed(npz_path, embeddings=matrix, sequence_ids=np.array([r["sequence_id"] for r in index_rows]))
    index_path = output_dir / out_cfg["embedding_index_csv"]
    write_csv(index_path, index_rows, list(index_rows[0].keys()))
    print(json.dumps({"status": "PASS", "embedding_npz": str(npz_path), "index_csv": str(index_path), "shape": list(matrix.shape)}, indent=2))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/plm_full_embedding_config_1_0.yaml")
    ap.add_argument("--package-root", default=".")
    ap.add_argument("--generate", action="store_true", help="Actually generate frozen ESM-2 embeddings after preflight PASS.")
    args = ap.parse_args()

    package_root = Path(args.package_root).resolve()
    config_path = package_root / args.config
    with config_path.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    report, order_rows = preflight(config, package_root)
    out_cfg = config["outputs"]
    qc_dir = package_root / out_cfg["qc_output_dir"]
    qc_dir.mkdir(parents=True, exist_ok=True)
    report_path = qc_dir / out_cfg["preflight_report_json"]
    order_qc_path = qc_dir / out_cfg["sequence_order_qc_csv"]
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    write_csv(order_qc_path, order_rows, list(order_rows[0].keys()) if order_rows else ["status"])

    print(json.dumps({"preflight_status": report["status"], "report": str(report_path), "sequence_order_qc": str(order_qc_path)}, indent=2))
    if report["status"] != "PASS":
        raise SystemExit("Preflight failed. Stop before embedding generation.")
    if args.generate:
        generate_embeddings(config, package_root)
    else:
        print("Validation-only mode complete. No ESM-2 embeddings generated.")


if __name__ == "__main__":
    main()
