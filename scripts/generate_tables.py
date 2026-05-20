#!/usr/bin/env python3
"""Manuscript table source inventory.

This utility reports the source CSV files included for tracing manuscript
tables and summary statistics. Final journal-formatted table rendering was
performed outside this pre-submission staging snapshot.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SOURCE_FILES = [
    "results/table6_plm_vs_aac.csv",
    "results/paired_stats.csv",
    "results/sensitivity_behavior.csv",
    "data/branch_summary.csv",
    "qc/qc_manifest.csv",
]


def main() -> int:
    print("Manuscript table/source CSV inventory")
    missing = []
    for rel in SOURCE_FILES:
        path = ROOT / rel
        status = "present" if path.exists() else "missing"
        print(f"- {rel}: {status}")
        if not path.exists():
            missing.append(rel)

    if missing:
        print("Missing source files:")
        for rel in missing:
            print(f"- {rel}")
        return 1

    print("All listed source files are present.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
