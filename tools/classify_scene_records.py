#!/usr/bin/env python3
from pathlib import Path
import argparse
from collections import Counter

p = argparse.ArgumentParser(description='Classify 4-byte records selected by the 9E70 index table')
p.add_argument('rom')
p.add_argument('--bank', type=int, default=22)
p.add_argument('--index-cpu', type=lambda x: int(x, 16), default=0x5F4C)
p.add_argument('--records-cpu', type=lambda x: int(x, 16), default=0x6046)
p.add_argument('--first-index', type=lambda x: int(x, 16), default=0x18)
p.add_argument('--last-index', type=lambda x: int(x, 16), default=0x30)
p.add_argument('--out', required=True)
a = p.parse_args()
rom = Path(a.rom).read_bytes()
bank = rom[a.bank*0x4000:(a.bank+1)*0x4000]
def cpu_off(cpu): return cpu - 0x4000
index_base = cpu_off(a.index_cpu)
record_base = cpu_off(a.records_cpu)
rows = []
for idx in range(a.first_index, a.last_index+1):
    eo = index_base + 2*(idx-a.first_index)
    ent = bank[eo:eo+2]
    if len(ent) != 2: continue
    word = ent[0] | ent[1]<<8
    ro = record_base + word
    rec = bank[ro:ro+4] if 0 <= ro < len(bank) else b''
    if len(rec) != 4:
        kind = 'outside'
    elif rec == b'\x00\x12\x00\x13' or rec[:2] == b'\x00\x12':
        kind = 'coordinate-or-range'
    elif rec[0] in (0xFC,0xFD,0xFE,0xFB,0xEE):
        kind = 'command-leading'
    elif rec[0] < 0x20 and rec[1] < 0x20:
        kind = 'small-parameters'
    elif rec[0] >= 0x80 or rec[1] >= 0x80:
        kind = 'high-byte-or-pointer'
    else:
        kind = 'mixed'
    rows.append((idx, word, ro, rec, kind))
counts = Counter(r[4] for r in rows)
out = ['# Scene record classification', '', f'bank={a.bank} index=0x{a.index_cpu:04X} records=0x{a.records_cpu:04X}', '', 'kind,count']
out.extend(f'{k},{v}' for k,v in sorted(counts.items()))
out += ['', 'index,entry_word,record_cpu,record_bytes,kind']
for idx, word, ro, rec, kind in rows:
    cpu = 0x4000 + ro if rec else 0
    out.append(f'0x{idx:02X},0x{word:04X},0x{cpu:04X},{rec.hex()},{kind}')
Path(a.out).write_text('\n'.join(out)+'\n', encoding='utf-8')
print(f'wrote {len(rows)} classified records to {a.out}')
