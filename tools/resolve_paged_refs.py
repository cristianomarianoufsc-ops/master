#!/usr/bin/env python3
from pathlib import Path
import re
import argparse

p = argparse.ArgumentParser(description='Resolve paged CPU references in a disassembly using nearby bank writes')
p.add_argument('asm')
p.add_argument('--out', required=True)
p.add_argument('--register', default='0ffffh')
args = p.parse_args()
lines = Path(args.asm).read_text(encoding='utf-8', errors='replace').splitlines()
bank = None
pending_bank = None
rows = []
for i, line in enumerate(lines):
    m = re.search(r'ld a,0([0-9a-f]+)h', line, re.I)
    if m:
        pending_bank = int(m.group(1), 16)
    if args.register.lower() in line.lower() and 'ld (' in line.lower() and pending_bank is not None:
        bank = pending_bank
        pending_bank = None
    if re.search(r'\b(call|jp|ld de|ld hl)\s+0?5[cC][0-9a-fA-F]{2}h', line):
        addr = re.search(r'0?([5][cC][0-9a-fA-F]{2})h', line).group(1)
        rows.append(f'line={i+1} bank_before={bank} cpu=0x{addr.upper()} instruction={line.strip()}')
Path(args.out).write_text('# Resolved paged references\n\n' + '\n'.join(rows) + '\n', encoding='utf-8')
print(f'wrote {len(rows)} resolved references to {args.out}')
