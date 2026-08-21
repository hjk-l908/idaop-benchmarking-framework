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


    paired = pd.read_csv(ROOT/'results/paired_stats.csv')
    random_rows = paired[paired['split_family'] == 'random_cv_R1_R10']
    if len(random_rows) != 24:
        errors.append(f'random-CV paired_stats should have 24 metric rows; observed {len(random_rows)}')
    if not (random_rows['n_pairs'] == 10).all():
        errors.append('random-CV paired_stats must use 10 replicate-level pairs')
    if not (random_rows['paired_test'] == 'paired_wilcoxon_replicate_level_two_sided').all():
        errors.append('random-CV paired_stats must declare replicate-level paired Wilcoxon testing')
    r02a_rows = paired[paired['split_family'] == 'r02a_sequence_cluster_hard_split']
    if len(r02a_rows) != 24 or not (r02a_rows['n_pairs'] == 4).all() or not (r02a_rows['paired_test'] == 'descriptive_only_n_lt_10').all():
        errors.append('R02A paired_stats rows must remain descriptive-only with n_pairs=4')
    key = random_rows[(random_rows['model']=='LR_L2') & (random_rows['analysis_branch']=='core_only') & (random_rows['metric']=='mcc')]
    if len(key) != 1:
        errors.append('missing corrected LR_L2/core_only/random-CV MCC paired-stat row')
    else:
        row = key.iloc[0]
        if abs(float(row['delta_mean']) - 0.0586807909950888) > 1e-12 or abs(float(row['p_value']) - 0.064453125) > 1e-12:
            errors.append('corrected LR_L2/core_only random-CV MCC paired statistics do not match the locked replicate-level values')

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
