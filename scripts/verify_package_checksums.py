#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMS = ROOT / 'metadata' / 'SHA256SUMS.txt'
SUMS_REL = SUMS.relative_to(ROOT).as_posix()
errors: list[str] = []
listed: set[str] = set()
checked = 0
total_entries = 0
inventory_loaded = False

try:
    inventory_text = SUMS.read_text(encoding='utf-8-sig')
    inventory_loaded = True
except Exception as exc:  # Always emit a machine-readable FAIL status.
    errors.append(f'unable to read checksum inventory: {exc}')
    inventory_text = ''

for line_number, raw in enumerate(inventory_text.splitlines(), start=1):
    if not raw.strip():
        continue
    total_entries += 1
    parts = raw.strip().split(maxsplit=1)
    if len(parts) != 2:
        errors.append(f'malformed inventory line {line_number}')
        continue
    expected, rel = parts
    rel = rel.lstrip('*').strip().replace('\\', '/')
    if len(expected) != 64 or any(ch not in '0123456789abcdefABCDEF' for ch in expected):
        errors.append(f'invalid sha256 on line {line_number}: {rel or "<missing path>"}')
        continue
    if not rel:
        errors.append(f'missing path on line {line_number}')
        continue
    if rel in listed:
        errors.append(f'duplicate inventory path: {rel}')
        continue
    listed.add(rel)

    path = (ROOT / rel).resolve()
    try:
        path.relative_to(ROOT.resolve())
    except ValueError:
        errors.append(f'path escapes repository root: {rel}')
        continue
    if not path.is_file():
        errors.append(f'missing: {rel}')
        continue
    observed = hashlib.sha256(path.read_bytes()).hexdigest()
    checked += 1
    if observed.lower() != expected.lower():
        errors.append(f'mismatch: {rel}')

# Reverse coverage check: every repository file except the inventory itself must be listed.
if inventory_loaded:
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [name for name in dirnames if name != '.git']
        base = Path(dirpath)
        for filename in filenames:
            rel = (base / filename).relative_to(ROOT).as_posix()
            if rel == SUMS_REL:
                continue
            if rel not in listed:
                errors.append(f'unlisted: {rel}')

status = 'PASS' if not errors else 'FAIL'
print(f'CHECKSUM_STATUS: {status}')
print(f'TOTAL_ENTRIES: {total_entries}')
print(f'CHECKED_FILES: {checked}')
if errors:
    print('ERRORS:')
    for item in errors:
        print(f'- {item}')
raise SystemExit(0 if not errors else 1)
