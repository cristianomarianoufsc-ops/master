#!/usr/bin/env python3
from pathlib import Path
import argparse
p=argparse.ArgumentParser(description='Catalog short streams B015-B07E')
p.add_argument('rom');p.add_argument('--bank',type=int,default=22);p.add_argument('--start',type=lambda x:int(x,16),default=0xB015);p.add_argument('--end',type=lambda x:int(x,16),default=0xB07E);p.add_argument('--out',required=True)
a=p.parse_args();rom=Path(a.rom).read_bytes();bank=rom[a.bank*0x4000:(a.bank+1)*0x4000]
def get(cpu,n=1): return bank[cpu-0x8000:cpu-0x8000+n]
seen=set();out=[]
for ptr in range(a.start,a.end+1):
 if ptr in seen: continue
 raw=get(ptr,64); end=raw.find(b'\xff'); seg=raw[:end+1] if end>=0 else raw
 if not seg: continue
 seen.update(range(ptr,ptr+len(seg)))
 nonzero=[f'{i:02X}:{v:02X}' for i,v in enumerate(seg[:-1]) if v]
 out.append(f'ptr=0x{ptr:04X} len={len(seg)} raw={seg.hex()} nonzero={" ".join(nonzero)}')
Path(a.out).write_text('\n'.join(out)+'\n',encoding='utf-8');print(f'wrote {len(out)} streams to {a.out}')
