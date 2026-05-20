#!/usr/bin/env python3
import argparse
import csv
from pathlib import Path

VALID = set("ACDEFGHIKLMNPQRSTVWY")

def parse_fasta_header(header):
    raw = header[1:].split()[0]
    parts = raw.split("|")
    if len(parts) >= 3:
        return parts[2]
    return raw

def read_fasta(path):
    seqs = []
    current_id = None
    current = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if current_id is not None:
                    seqs.append((current_id, "".join(current).upper()))
                current_id = parse_fasta_header(line)
                current = []
            else:
                current.append(line.upper())
        if current_id is not None:
            seqs.append((current_id, "".join(current).upper()))
    return seqs

def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fields = reader.fieldnames or []
    return fields, rows

def choose_id_col(fields):
    if "sequence_id" in fields:
        return "sequence_id"
    if "id" in fields:
        return "id"
    return fields[0]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--fasta", required=True)
    ap.add_argument("--order", required=True)
    args = ap.parse_args()

    for p in [args.csv, args.fasta, args.order]:
        if not Path(p).exists():
            print("FAIL: missing file", p)
            return 2

    csv_fields, csv_rows = read_csv(args.csv)
    order_fields, order_rows = read_csv(args.order)
    fasta_rows = read_fasta(args.fasta)

    csv_id_col = choose_id_col(csv_fields)
    order_id_col = "sequence_id" if "sequence_id" in order_fields else choose_id_col(order_fields)

    csv_ids = [r[csv_id_col].strip() for r in csv_rows]
    csv_seqs = [r.get("sequence", "").strip().upper() for r in csv_rows]
    fasta_ids = [sid for sid, seq in fasta_rows]
    fasta_seqs = [seq for sid, seq in fasta_rows]
    order_ids = [r[order_id_col].strip() for r in order_rows]

    ok = True

    if len(set(csv_ids)) != len(csv_ids):
        print("FAIL: duplicate IDs in CSV")
        ok = False

    if len(set(fasta_ids)) != len(fasta_ids):
        print("FAIL: duplicate IDs in FASTA")
        ok = False

    if csv_ids != fasta_ids:
        print("FAIL: CSV and FASTA sequence_id order mismatch")
        for i, (c, f) in enumerate(zip(csv_ids, fasta_ids), start=1):
            if c != f:
                print("first_id_mismatch_row:", i, "csv:", c, "fasta:", f)
                break
        ok = False

    if csv_seqs != fasta_seqs:
        print("FAIL: CSV and FASTA sequence string order mismatch")
        for i, (c, f) in enumerate(zip(csv_seqs, fasta_seqs), start=1):
            if c != f:
                print("first_sequence_mismatch_row:", i, "csv:", c, "fasta:", f)
                break
        ok = False

    if order_ids and order_ids != csv_ids:
        print("FAIL: order manifest and CSV order mismatch")
        for i, (o, c) in enumerate(zip(order_ids, csv_ids), start=1):
            if o != c:
                print("first_order_mismatch_row:", i, "order:", o, "csv:", c)
                break
        ok = False

    for sid, seq in fasta_rows:
        bad = sorted(set(seq) - VALID)
        if not seq:
            print("FAIL: empty sequence", sid)
            ok = False
        if bad:
            print("FAIL: invalid residues", sid, "".join(bad))
            ok = False

    print("csv_rows:", len(csv_rows))
    print("fasta_records:", len(fasta_rows))
    print("sequence_id_order_match:", csv_ids == fasta_ids)
    print("sequence_string_order_match:", csv_seqs == fasta_seqs)
    print("order_manifest_match:", order_ids == csv_ids)
    print("validation_status:", "PASS" if ok else "FAIL")
    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
