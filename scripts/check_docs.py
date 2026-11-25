from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parent.parent
files = (
    sorted(root.glob('*.md'))
    + sorted((root / 'docs').rglob('*.md'))
    + sorted((root / 'third_party').glob('*.md'))
)
errors = []
links = 0
for file in files:
    text = file.read_text(encoding='utf-8')
    if not text.endswith('\n'):
        errors.append(f'{file.relative_to(root)}: missing final newline')
    if text.count('```') % 2:
        errors.append(f'{file.relative_to(root)}: unmatched code fence')
    for target in re.findall(r'\]\(([^)]+)\)', text):
        if re.match(r'^[a-z][a-z0-9+.-]*:', target, flags=re.I):
            continue
        path = target.split('#', 1)[0]
        if path and not (file.parent / path).exists():
            errors.append(f'{file.relative_to(root)}: broken local link {target}')
        links += 1

spec = (root / 'docs/functional-spec.md').read_text(encoding='utf-8')
ids = re.findall(r'^\| ([A-Z]+-\d+) \|', spec, flags=re.M)
if len(ids) != len(set(ids)):
    errors.append('Duplicate requirement IDs')
rows = [line for line in spec.splitlines() if re.match(r'^\| [A-Z]+-\d+ \|', line)]
for row in rows:
    fields = [v.strip() for v in row.split('|')[1:-1]]
    if len(fields) != 4 or not re.search(r'M[0-6]', fields[2]) or not fields[3]:
        errors.append(f'Invalid requirement row: {row}')
for file in files:
    for req in re.findall(r'\b[A-Z]{2,}-\d{2}\b', file.read_text(encoding='utf-8')):
        if req.startswith('ADR-'):
            continue
        if req not in ids:
            errors.append(f'{file.relative_to(root)}: undefined requirement {req}')

print(f'Markdown files: {len(files)}; local links: {links}; requirements: {len(ids)}')
for error in errors:
    print(error)
if errors:
    sys.exit(1)
print('Documentation checks passed.')
