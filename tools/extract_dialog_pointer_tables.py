#!/usr/bin/env python3
from pathlib import Path
import argparse
p=argparse.ArgumentParser(description='Extract dialogue pointers resolved by 05C16')
p.add_argument('rom');p.add_argument('--bank',type=int,default=22);p.add_argument('--table',type=lambda x:int(x,16),default=0xaf55);p.add_argument('--first',type=lambda x:int(x,0),default=0);p.add_argument('--last',type=lambda x:int(x,0),default=0x40);p.add_argument('--out',required=True)
a=p.parse_args();rom=Path(a.rom).read_bytes();bank=rom[a.bank*0x4000:(a.bank+1)*0x4000]
def b(cpu,n=1): return bank[cpu-0x8000:cpu-0x8000+n]
out=[]
for c in range(a.first,a.last+1):
 pos=a.table-0x8000+2*c
 if pos<0 or pos+2>len(bank): continue
 ptr=int.from_bytes(bank[pos:pos+2],'little')
 if not 0x8000<=ptr<0xc000: out.append(f'C205=0x{c:02X} ptr=0x{ptr:04X} invalid');continue
 raw=b(ptr,0x100)
 end=raw.find(b'\xff')
 if end<0: end=min(len(raw),0x100)
 seg=raw[:end+1]
 fn=Path(a.out).with_suffix('');fn=fn.parent/(fn.name+f'_c205_{c:02X}.bin');fn.write_bytes(seg)
 out.append(f'C205=0x{c:02X} table=0x{a.table+2*c:04X} ptr=0x{ptr:04X} len={len(seg)} hex={seg[:64].hex()}')
Path(a.out).write_text('\n'.join(out)+'\n',encoding='utf-8');print(f'wrote {len(out)} entries to {a.out}')
