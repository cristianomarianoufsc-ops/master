#!/usr/bin/env python3
from pathlib import Path
import argparse

p=argparse.ArgumentParser(description='Tokenize conserved scene command streams')
p.add_argument('rom'); p.add_argument('--bank',type=int,default=22); p.add_argument('--start',type=lambda x:int(x,16),default=0x9d08); p.add_argument('--end',type=lambda x:int(x,16),default=0x9fc8); p.add_argument('--out',required=True)
a=p.parse_args()
rom=Path(a.rom).read_bytes(); base=a.bank*0x4000; data=rom[base+a.start-0x8000:base+a.end-0x8000+1]
control={0xfb:'FB',0xfc:'FC',0xfd:'FD',0xfe:'FE',0xff:'FF',0xee:'EE'}
out=['# Conservative scene command tokens','',f'bank={a.bank} range=0x{a.start:04X}-0x{a.end:04X}','']
pos=0; token=0
while pos<len(data):
 v=data[pos]
 if v in control:
  out.append(f'{token:03d} cpu=0x{a.start+pos:04X} {control[v]}')
  token+=1; pos+=1
 else:
  j=pos+1
  while j<len(data) and data[j] not in control: j+=1
  out.append(f'{token:03d} cpu=0x{a.start+pos:04X} PAYLOAD len={j-pos} bytes={data[pos:j].hex()}')
  token+=1; pos=j
Path(a.out).write_text('\n'.join(out)+'\n',encoding='utf-8')
print(f'wrote {token} tokens to {a.out}')
