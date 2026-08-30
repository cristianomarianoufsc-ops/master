#!/usr/bin/env python3
from pathlib import Path
import re
import argparse

p = argparse.ArgumentParser(description='Extract IX+18 dispatch states and nearby handler targets')
p.add_argument('asm')
p.add_argument('--out', required=True)
args = p.parse_args()
lines = Path(args.asm).read_text(encoding='utf-8', errors='replace').splitlines()
rows = []
for i, line in enumerate(lines):
    if re.search(r'ld \(ix\+018h\),', line, re.I) or re.search(r'ld \(ix\+018h\)', line, re.I):
        context = []
        for j in range(max(0, i-4), min(len(lines), i+7)):
            context.append(lines[j].strip())
        rows.append((i+1, line.strip(), context))
out = ['# IX+18 dispatch candidates', '', 'The fixed-bank dispatcher at 3954 loads IX+18, calls RST 10h, and jumps through HL.', '']
for n, (line_no, instr, context) in enumerate(rows, 1):
    out.append(f'## {n}. line {line_no}: {instr}')
    out.extend('    ' + x for x in context)
    out.append('')
Path(args.out).write_text('\n'.join(out), encoding='utf-8')
print(f'wrote {len(rows)} IX+18 dispatch candidates to {args.out}')
