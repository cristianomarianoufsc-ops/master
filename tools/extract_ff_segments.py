#!/usr/bin/env python3
from pathlib import Path
import argparse

p = argparse.ArgumentParser(description='Extract FF-terminated segments from a ROM bank')
p.add_argument('rom')
p.add_argument('--bank', type=int, default=22)
p.add_argument('--start', type=lambda x: int(x, 16), default=0x5F40)
p.add_argument('--end', type=lambda x: int(x, 16), default=0x789D)
p.add_argument('--min-len', type=int, default=4)
p.add_argument('--max-len', type=int, default=512)
p.add_argument('--out', required=True)
a = p.parse_args()
rom = Path(a.rom).read_bytes()
base = a.bank * 0x4000
lo = base + a.start - 0x4000
hi = base + a.end - 0x4000
buf = rom[lo:hi]
out = []
seg_start = 0
for i, value in enumerate(buf):
    if value != 0xFF:
        continue
    seg = buf[seg_start:i]
    if a.min_len <= len(seg) <= a.max_len:
        low = bytes(x for x in seg if 0 < x < 0x80)
        file_off = lo + seg_start
        cpu = 0x4000 + (file_off - base)
        out.append(f'bank={a.bank:02d} cpu=0x{cpu:04X} file=0x{file_off:06X} len={len(seg)} low_count={len(low)} raw={seg.hex()} low={low.hex()}')
    seg_start = i + 1
Path(a.out).write_text('\n'.join(out) + ('\n' if out else ''), encoding='utf-8')
print(f'wrote {len(out)} FF-terminated segments to {a.out}')
