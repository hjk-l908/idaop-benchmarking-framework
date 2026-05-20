#!/usr/bin/env python3
import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
errors = []
warnings = []

required_files = [
    'data/branch_manifest.csv',
    'splits/random_cv_R1_R10_manifest.csv',
    'splits/r02a_hard_split_manifest.csv',
    'splits/PILOT_R02A_sequence_cluster_hard_split_assignments.csv',
    'results/table6_plm_vs_aac.csv',
    'results/paired_stats.csv',
    'results/sensitivity_behavior.csv',
    'qc/qc_manifest.csv',
    'supplementary/R02A_retained_assignment_documentation_1_0.md',
]
for rel in required_files:
    if not (ROOT/rel).exists():
        errors.append(f'missing required file: {rel}')

if not errors:
    branch = pd.read_csv(ROOT/'data/branch_manifest.csv')
    expected_counts = {'positive_core': 899, 'core_negative': 29, 'negative_sensitivity': 3, 'challenge_only': 28}
    observed = branch['branch'].value_counts().to_dict()
    for branch_name, expected in expected_counts.items():
        if int(observed.get(branch_name, 0)) != expected:
            errors.append(f'branch count mismatch for {branch_name}: expected {expected}, observed {observed.get(branch_name, 0)}')
    if branch['sequence_id'].duplicated().any():
        errors.append('duplicate sequence_id in data/branch_manifest.csv')

    for rel in ['splits/random_cv_R1_R10_manifest.csv', 'splits/r02a_hard_split_manifest.csv']:
        df = pd.read_csv(ROOT/rel)
        if (df['branch'] == 'challenge_only').any():
            errors.append(f'challenge_only row found in train/test manifest: {rel}')

    table6 = pd.read_csv(ROOT/'results/table6_plm_vs_aac.csv')
    if len(table6) != 8:
        errors.append(f'Table 6 should have 8 rows; observed {len(table6)}')
    required_table6 = [
        ('LR_L2','r02a_sequence_cluster_hard_split','core_only'),
        ('LinearSVM','r02a_sequence_cluster_hard_split','core_only'),
    ]
    for model, split, branch_name in required_table6:
        ok = ((table6['model']==model) & (table6['split_family']==split) & (table6['analysis_branch']==branch_name)).any()
        if not ok:
            errors.append(f'missing Table 6 row: {model}/{split}/{branch_name}')

status = 'PASS' if not errors else 'FAIL'
print(f'VALIDATION_STATUS: {status}')
if warnings:
    print('WARNINGS:')
    for w in warnings:
        print(f'- {w}')
if errors:
    print('ERRORS:')
    for e in errors:
        print(f'- {e}')
raise SystemExit(0 if not errors else 1)
