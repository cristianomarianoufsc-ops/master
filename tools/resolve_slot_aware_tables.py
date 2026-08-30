#!/usr/bin/env python3
from pathlib import Path
import argparse
p=argparse.ArgumentParser(description='Resolve paged references with explicit CPU slot')
p.add_argument('rom');p.add_argument('--bank',type=int,required=True);p.add_argument('--cpu',type=lambda x:int(x,16),required=True);p.add_argument('--slot',choices=['4000','8000'],required=True);p.add_argument('--length',type=int,default=64);p.add_argument('--out',required=True)
a=p.parse_args();rom=Path(a.rom).read_bytes();data=rom[a.bank*0x4000:(a.bank+1)*0x4000];base=int(a.slot,16);off=a.cpu-base
if off<0 or off>=len(data): raise SystemExit('address outside selected slot')
chunk=data[off:off+a.length]
lines=[f'bank={a.bank}',f'cpu=0x{a.cpu:04X}',f'slot=0x{base:04X}',f'file_offset=0x{a.bank*0x4000+off:06X}',f'bytes={chunk.hex()}','']
for i in range(0,len(chunk)-1,2):
 w=chunk[i]|chunk[i+1]<<8
 if 0x4000<=w<0xc000: lines.append(f'+0x{i:02X}: word=0x{w:04X} slot={("4000" if w<0x8000 else "8000")}')
Path(a.out).write_text('\n'.join(lines)+'\n',encoding='utf-8');print(f'wrote {a.out}')
