#!/usr/bin/env python3
"""Traditional AAC baseline source inventory.

The manuscript reports locked AAC_reference baseline results. This utility
does not rerun model training; it checks that the source result and split
files needed to trace the reported baseline comparisons are present in this
pre-submission staging package.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SOURCE_FILES = [
    "results/table6_plm_vs_aac.csv",
    "results/paired_stats.csv",
    "splits/random_cv_R1_R10_manifest.csv",
    "splits/r02a_hard_split_manifest.csv",
    "data/branch_manifest.csv",
]


def main() -> int:
    print("Traditional AAC baseline source inventory")
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
