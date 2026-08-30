#!/usr/bin/env python3
from pathlib import Path
import re
import argparse

p = argparse.ArgumentParser(description='List bank-register writes and nearby CPU addresses in a disassembly')
p.add_argument('asm')
p.add_argument('--register', default='0ffffh')
p.add_argument('--out', required=True)
a = p.parse_args()
lines = Path(a.asm).read_text(encoding='utf-8', errors='replace').splitlines()
rows = []
last_bank = None
for i, line in enumerate(lines):
    m = re.search(r'ld a,0([0-9a-f]+)h', line, re.I)
    if m:
        last_bank = int(m.group(1), 16)
    if a.register.lower() in line.lower() and 'ld (' in line.lower():
        context = []
        for j in range(max(0, i-5), min(len(lines), i+8)):
            context.append(lines[j].strip())
        rows.append({'line': i+1, 'bank_value_before': last_bank, 'write': line.strip(), 'context': context})
out = ['# Bank-switch contexts', '']
for n, row in enumerate(rows, 1):
    out.append(f"## {n}. line {row['line']} bank={row['bank_value_before']!s}")
    out.extend('    ' + x for x in row['context'])
    out.append('')
Path(a.out).write_text('\n'.join(out), encoding='utf-8')
print(f'wrote {len(rows)} contexts to {a.out}')
