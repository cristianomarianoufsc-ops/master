#!/usr/bin/env python3
from pathlib import Path
import argparse
p=argparse.ArgumentParser(description='Exact 04CFD emulator')
p.add_argument('rom');p.add_argument('--bank',type=int,default=19);p.add_argument('--table',type=lambda x:int(x,16),required=True);p.add_argument('--c',type=lambda x:int(x,0),required=True);p.add_argument('--out',required=True)
a=p.parse_args();rom=Path(a.rom).read_bytes();data=rom[a.bank*0x4000:(a.bank+1)*0x4000]
def read(cpu,n=1): return data[cpu-0x8000:cpu-0x8000+n]
ram={x:0 for x in range(0xd120,0xd140)}
hl=a.table; count=read(hl)[0];hl+=1;c=a.c&0xff;records=[]
for _ in range(count):
 de=read(hl)[0]|read(hl+1)[0]<<8;hl+=2;mask=read(hl)[0];hl+=1
 old=c;c=((c>>1)|((c&1)<<7))&0xff;carry=old&1
 before=ram.get(de,0)
 if de in ram:
  if carry: ram[de]=before|mask
  else: ram[de]=before&(~mask&0xff)
 records.append(f'target=0x{de:04X} mask=0x{mask:02X} c_before=0x{old:02X} carry={carry} value=0x{ram.get(de,0):02X}')
out=[f'# Exact 04CFD emulation',f'bank={a.bank} table=0x{a.table:04X} initial_C=0x{a.c:02X} count={count}','']+records+['','## resulting RAM']
for addr in sorted(ram): out.append(f'0x{addr:04X},0x{ram[addr]:02X}')
Path(a.out).write_text('\n'.join(out)+'\n',encoding='utf-8');print(f'wrote {a.out}')
