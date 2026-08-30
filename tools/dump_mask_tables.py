#!/usr/bin/env python3
from pathlib import Path
import argparse

p=argparse.ArgumentParser(description='Dump count/(address,mask) records from mask tables')
p.add_argument('rom'); p.add_argument('--bank',type=int,default=21); p.add_argument('--cpu',type=lambda x:int(x,16),default=0xac31); p.add_argument('--length',type=int,default=96); p.add_argument('--out',required=True)
a=p.parse_args();rom=Path(a.rom).read_bytes();data=rom[a.bank*0x4000+a.cpu-0x8000:]
out=['# Mask table records','',f'bank={a.bank} cpu=0x{a.cpu:04X}','']
pos=0; table=0
while pos<len(data) and pos<a.length:
 count=data[pos]; pos+=1
 if count==0: out.append(f'table={table} offset=0x{pos-1:X} count=0'); break
 out.append(f'table={table} offset=0x{pos-1:X} count={count}')
 for i in range(count):
  if pos+2>=len(data): break
  addr=data[pos]|data[pos+1]<<8; mask=data[pos+2]; pos+=3
  out.append(f'  {i:02d}: target=0x{addr:04X} mask=0x{mask:02X}')
 out.append('');table+=1
Path(a.out).write_text('\n'.join(out)+'\n',encoding='utf-8')
print(f'wrote {table} tables to {a.out}')
