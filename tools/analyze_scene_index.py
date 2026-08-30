#!/usr/bin/env python3
from pathlib import Path
import argparse

p = argparse.ArgumentParser(description='Analyze the 9E70 scene index indirection')
p.add_argument('rom')
p.add_argument('--bank', type=int, default=22)
p.add_argument('--index-cpu', type=lambda x: int(x, 16), default=0x5F4C)
p.add_argument('--records-cpu', type=lambda x: int(x, 16), default=0x6046)
p.add_argument('--first-index', type=lambda x: int(x, 16), default=0x18)
p.add_argument('--last-index', type=lambda x: int(x, 16), default=0x30)
p.add_argument('--out', required=True)
a = p.parse_args()
rom = Path(a.rom).read_bytes()
base = a.bank * 0x4000
bank_data = rom[base:base + 0x4000]
def read_cpu(cpu, n):
    off = cpu - 0x4000
    return bank_data[off:off+n]
index_base = a.index_cpu - 0x4000
record_base = a.records_cpu - 0x4000
out = []
out.append('# 9E70 scene-index analysis')
out.append('')
out.append('index,entry_offset,entry_word,record_cpu,record_bytes,record_kind')
for idx in range(a.first_index, a.last_index + 1):
    ent_off = index_base + 2 * (idx - a.first_index)
    ent = bank_data[ent_off:ent_off+2]
    if len(ent) < 2:
        break
    word = ent[0] | (ent[1] << 8)
    rec_off = record_base + word
    if 0 <= rec_off < len(bank_data):
        rec = bank_data[rec_off:rec_off+4]
        rec_cpu = 0x4000 + rec_off
        kind = 'in-bank' if len(rec) == 4 else 'truncated'
    else:
        rec = b''
        rec_cpu = 0
        kind = 'outside-bank'
    out.append(f'0x{idx:02X},0x{0x4000+ent_off:04X},0x{word:04X},0x{rec_cpu:04X},{rec.hex()},{kind}')
Path(a.out).write_text('\n'.join(out) + '\n', encoding='utf-8')
print(f'wrote {a.last_index-a.first_index+1} index rows to {a.out}')
