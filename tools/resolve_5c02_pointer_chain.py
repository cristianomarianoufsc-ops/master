#!/usr/bin/env python3
from pathlib import Path
import argparse
p=argparse.ArgumentParser(description='Resolve 05C02 pointer chains')
p.add_argument('rom');p.add_argument('--bank',type=int,default=22);p.add_argument('--table',type=lambda x:int(x,16),required=True);p.add_argument('--out',required=True);p.add_argument('--max',type=int,default=64)
a=p.parse_args();rom=Path(a.rom).read_bytes();bank=rom[a.bank*0x4000:(a.bank+1)*0x4000]
def get(cpu,n=1): return bank[cpu-0x8000:cpu-0x8000+n]
out=[];hl=a.table
for i in range(a.max):
 if not 0x8000<=hl<0xc000 or hl-0x8000+2>len(bank): out.append(f'{i}: invalid table hl=0x{hl:04X}');break
 de=int.from_bytes(get(hl,2),'little'); out.append(f'{i}: table=0x{hl:04X} target=0x{de:04X} first={get(de,8).hex() if 0x8000<=de<0xc000 else "invalid"}')
 hl+=2
 if 0x8000<=de<0xc000 and get(de,1)[0]==0:
  if hl-0x8000+2<=len(bank): final=int.from_bytes(get(hl,2),'little');out.append(f'final=0x{final:04X} bytes={get(final,64).hex() if 0x8000<=final<0xc000 else "invalid"}')
  break
Path(a.out).write_text('\n'.join(out)+'\n',encoding='utf-8');print(f'wrote {a.out}')
