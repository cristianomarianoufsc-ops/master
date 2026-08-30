#!/usr/bin/env python3
from pathlib import Path
import argparse

p=argparse.ArgumentParser(description='Parse scene stream while preserving command bytes')
p.add_argument('rom'); p.add_argument('--bank',type=int,default=22); p.add_argument('--start',type=lambda x:int(x,16),default=0x5f40); p.add_argument('--length',type=lambda x:int(x,16),default=0x200); p.add_argument('--out',required=True)
a=p.parse_args()
rom=Path(a.rom).read_bytes(); base=a.bank*0x4000+(a.start-0x4000); raw=rom[base:base+a.length]
out=['# Scene stream command-preserving parse','',f'bank={a.bank} start=0x{a.start:04X} length=0x{a.length:X}','', 'offset,byte,classification']
for i,v in enumerate(raw):
 if v==0xff: c='record/end marker'
 elif v==0x00: c='padding/zero candidate'
 elif v in (0xfb,0xfc,0xfd,0xfe,0xee): c='control candidate'
 elif v in (0x05,0x06,0x10,0x20): c='common parameter/opcode candidate'
 else: c='payload/unknown'
 out.append(f'0x{a.start+i:04X},0x{v:02X},{c}')
Path(a.out).write_text('\n'.join(out)+'\n',encoding='utf-8')
print(f'wrote {len(raw)} bytes to {a.out}')
