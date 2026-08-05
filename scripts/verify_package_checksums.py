#!/usr/bin/env python3
from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMS = ROOT / 'metadata' / 'SHA256SUMS.txt'
errors = []
checked = 0

for raw in SUMS.read_text(encoding='utf-8').splitlines():
    if not raw.strip():
        continue
    expected, rel = raw.split('  ', 1)
    path = ROOT / rel
    if not path.is_file():
        errors.append(f'missing: {rel}')
        continue
    observed = hashlib.sha256(path.read_bytes()).hexdigest()
    checked += 1
    if observed != expected:
        errors.append(f'mismatch: {rel}')

status = 'PASS' if not errors else 'FAIL'
print(f'CHECKSUM_STATUS: {status}')
print(f'CHECKED_FILES: {checked}')
if errors:
    print('ERRORS:')
    for item in errors:
        print(f'- {item}')
raise SystemExit(0 if not errors else 1)
