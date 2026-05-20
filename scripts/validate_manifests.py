#!/usr/bin/env python3
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
required = [
    ROOT / "data" / "branch_manifest.csv",
    ROOT / "splits" / "random_cv_R1_R10_manifest.csv",
    ROOT / "splits" / "r02a_hard_split_manifest.csv",
]

errors = []
for path in required:
    if not path.exists():
        errors.append(f"missing: {path}")

if not errors:
    branch = pd.read_csv(ROOT / "data" / "branch_manifest.csv")
    if "sequence_id" not in branch.columns:
        errors.append("branch_manifest.csv missing sequence_id column")
    for p in required[1:]:
        df = pd.read_csv(p)
        if (df.get("branch", pd.Series(dtype=str)).astype(str) == "challenge_only").any():
            errors.append(f"challenge_only appears in train/CV split manifest: {p}")

if errors:
    print("VALIDATION_STATUS: FAIL")
    for e in errors:
        print("ERROR:", e)
    raise SystemExit(1)
print("VALIDATION_STATUS: PASS")
