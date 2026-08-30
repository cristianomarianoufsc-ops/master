#!/usr/bin/env python3
from pathlib import Path
import argparse

p = argparse.ArgumentParser(description='Extract candidate 2-byte glyph streams from an SMS ROM bank')
p.add_argument('rom')
p.add_argument('--bank', type=int, default=22)
p.add_argument('--start', type=lambda x: int(x, 16), default=0x5F40)
p.add_argument('--end', type=lambda x: int(x, 16), default=0x789D)
p.add_argument('--max-pairs', type=int, default=96)
p.add_argument('--out', required=True)
a = p.parse_args()
rom = Path(a.rom).read_bytes()
base = a.bank * 0x4000
lo = base + a.start - 0x4000
hi = base + a.end - 0x4000
buf = rom[lo:hi]
lines = []
for pos in range(0, len(buf) - 1, 2):
    pairs = []
    for j in range(a.max_pairs):
        k = pos + 2*j
        if k + 1 >= len(buf):
            break
        x, y = buf[k], buf[k+1]
        pairs.append((x,y))
        if x == 0xFF:
            break
    if pairs and pairs[-1][0] == 0xFF and len(pairs) >= 3:
        xs = ''.join(f'{x:02X}' for x,y in pairs)
        ys = ''.join(f'{y:02X}' for x,y in pairs)
        nonzero = sum(x != 0 for x,y in pairs[:-1])
        if nonzero >= 2:
            file_off = lo + pos
            cpu = 0x4000 + (file_off - base)
            lines.append(f'bank={a.bank:02d} cpu=0x{cpu:04X} file=0x{file_off:06X} pairs={len(pairs)-1:02d} glyph_bytes={xs[:-2]} attrs={ys[:-2]} raw={bytes(sum(([x,y] for x,y in pairs), [])).hex()}')
Path(a.out).write_text('\n'.join(lines) + ('\n' if lines else ''), encoding='utf-8')
print(f'wrote {len(lines)} candidates to {a.out}')
