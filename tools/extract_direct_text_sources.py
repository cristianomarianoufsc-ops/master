#!/usr/bin/env python3
from pathlib import Path
import argparse
import re

p = argparse.ArgumentParser(description='Extract direct C223/C238 text-source addresses from bank 21')
p.add_argument('rom')
p.add_argument('--bank', type=int, default=22)
p.add_argument('--asm', default='build/bank21.asm')
p.add_argument('--length', type=int, default=256)
p.add_argument('--out', required=True)
a = p.parse_args()
rom = Path(a.rom).read_bytes()
asm = Path(a.asm).read_text(encoding='utf-8', errors='replace').splitlines()
base = a.bank * 0x4000
bank = rom[base:base+0x4000]
seen = set()
rows = []
for i, line in enumerate(asm):
    if not re.search(r'ld hl,0[0-9a-f]+h', line, re.I):
        continue
    m = re.search(r'ld hl,0([0-9a-f]+)h', line, re.I)
    if not m:
        continue
    addr = int(m.group(1), 16)
    if not (0x4000 <= addr < 0x8000):
        continue
    nearby = '\n'.join(asm[i:min(i+6, len(asm))])
    if not re.search(r'0c223h|0c238h', nearby, re.I):
        continue
    if addr in seen:
        continue
    seen.add(addr)
    off = addr - 0x4000
    raw = bank[off:off+a.length]
    end = raw.find(b'\xff')
    visible = raw if end < 0 else raw[:end+1]
    rows.append((i+1, addr, visible, end))
out = ['# Direct text-source candidates', '', f'bank={a.bank} count={len(rows)}', '']
for line_no, addr, raw, end in rows:
    out.append(f'line={line_no} cpu=0x{addr:04X} terminator_offset={end} raw={raw.hex()}')
Path(a.out).write_text('\n'.join(out)+'\n', encoding='utf-8')
print(f'wrote {len(rows)} direct source candidates to {a.out}')
