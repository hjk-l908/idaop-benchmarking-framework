# Repository safety-search and manifest update commands

Run these from the root of the clean public repository after copying in `results/diagnostic/`.

## 1. Copy diagnostic folder into the clean repo

```bash
# From the extracted patch folder:
rsync -av results/diagnostic/ /path/to/idaop-benchmarking-framework/results/diagnostic/
```

## 2. Rebuild or append SHA-256 checksums

If the repository checksum file is intended to cover the whole repo, rebuild it from the repo root:

```bash
find data metadata results scripts supplementary docs -type f \
  ! -path '.git/*' \
  -print0 | sort -z | xargs -0 sha256sum > metadata/SHA256SUMS.txt
```

If you only need to append the diagnostic entries, append the fragment supplied in this patch and then sort/deduplicate:

```bash
cat metadata/SHA256SUMS_diagnostic_v2_0_append.txt >> metadata/SHA256SUMS.txt
sort -k2,2 -u metadata/SHA256SUMS.txt -o metadata/SHA256SUMS.txt
```

## 3. Update `metadata/package_file_manifest.csv`

If the repository already has a full manifest, append the diagnostic fragment supplied in this patch after verifying compatible columns. A safe command-line approach is:

```bash
python - <<'PYCODE'
from pathlib import Path
import pandas as pd
root = Path('.')
main = root / 'metadata' / 'package_file_manifest.csv'
append = root / 'metadata' / 'package_file_manifest_diagnostic_v2_0_append.csv'
base = pd.read_csv(main) if main.exists() else pd.DataFrame()
add = pd.read_csv(append)
if base.empty:
    out = add
else:
    for c in add.columns:
        if c not in base.columns:
            base[c] = ''
    for c in base.columns:
        if c not in add.columns:
            add[c] = ''
    out = pd.concat([base, add[base.columns]], ignore_index=True)
    if 'relative_path' in out.columns:
        out = out.drop_duplicates(subset=['relative_path'], keep='last')
out.to_csv(main, index=False)
print(f'Wrote {main} with {len(out)} rows')
PYCODE
```

## 4. Required safety searches before public release

```bash
grep -RInE '/home|/home/l908|l908|antioxidant_peptide_benchmark|plm_execution|password|token|TODO|TO_BE_CONFIRMED|placeholder|C:\Users|Users\|過程' . \
  --exclude-dir=.git \
  --exclude='repo_safety_search_commands.md' \
  --exclude='diagnostic_patch_validation_report.md' \
  --exclude='*.png' --exclude='*.tif' --exclude='*.jpg' --exclude='*.jpeg' --exclude='*.pdf' --exclude='*.docx' --exclude='*.zip'
```

Interpretation:

- Any hit in `results/diagnostic/*.csv` should block release until reviewed and scrubbed.
- `TODO`, `placeholder`, or `TO_BE_CONFIRMED` hits may be acceptable only in draft/admin files that will not be publicly released.
- Do not publish the original internal server-process archive.
- Do not publish R08 as evidence; it should remain documented as attempted but not interpretable because no usable metric output was available.

## 5. Optional GitHub code search queries after pushing a private branch

Use these exact search terms in GitHub repository search:

```text
/home
/home/l908
l908
antioxidant_peptide_benchmark
plm_execution
password
token
TODO
TO_BE_CONFIRMED
placeholder
過程
```
