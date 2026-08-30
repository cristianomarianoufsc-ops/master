#!/usr/bin/env python3
from pathlib import Path
import argparse

p=argparse.ArgumentParser(description='Resolve C208 scene indices into banked pointers')
p.add_argument('rom'); p.add_argument('--bank',type=int,default=22); p.add_argument('--records-cpu',type=lambda x:int(x,16),default=0x6046); p.add_argument('--out',required=True)
a=p.parse_args()
rom=Path(a.rom).read_bytes(); bank=rom[a.bank*0x4000:(a.bank+1)*0x4000]
def b(cpu,n=1): return bank[cpu-0x4000:cpu-0x4000+n]
rows=[]
# C208 is consumed as a 16-bit value and transformed by the 0x170 threshold.
for idx in range(0,0x100):
    # Treat idx as the low-byte index into the four-byte record area for an initial census.
    cpu=a.records_cpu+idx*4
    raw=b(cpu,3)
    if len(raw)<3: continue
    value=raw[0]|(raw[1]<<8)
    page=0x1e
    adjusted=value
    if value>=0x170:
        adjusted=value-0x170; page=0x1f
    rows.append((idx,cpu,raw.hex(),value,adjusted,page))
out=['# C208 to FFFF page-resolution census','', 'index,record_cpu,raw3,c208,adjusted,ffff_page']
for r in rows: out.append(f'0x{r[0]:02X},0x{r[1]:04X},{r[2]},0x{r[3]:04X},0x{r[4]:04X},0x{r[5]:02X}')
Path(a.out).write_text('\n'.join(out)+'\n',encoding='utf-8')
print(f'wrote {len(rows)} rows to {a.out}')
