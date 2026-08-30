#!/usr/bin/env python3
from pathlib import Path
import argparse

p=argparse.ArgumentParser(description='Extract RST 10h vector table candidates')
p.add_argument('rom'); p.add_argument('--start',type=lambda x:int(x,16),default=0x8000); p.add_argument('--count',type=int,default=32); p.add_argument('--out',required=True)
a=p.parse_args(); rom=Path(a.rom).read_bytes(); fixed=rom[:0x4000]
# RST 10h receives HL as table base and A as selector; this report enumerates
# common table locations in the paged scene bank for later correlation.
out=['# RST 10h vector-table candidates','',f'fixed_vector=0x0010 count={a.count}','']
for bank in (1,13,19,21,22,23):
 data=rom[bank*0x4000:(bank+1)*0x4000]
 off=a.start-0x8000
 if off<0 or off>=len(data): continue
 out.append(f'## bank {bank} base 0x{a.start:04X}')
 for i in range(a.count):
  pos=off+i*2; pair=data[pos:pos+2]
  if len(pair)<2: break
  val=pair[0]|pair[1]<<8
  out.append(f'index=0x{i:02X} cpu=0x{a.start+i*2:04X} word=0x{val:04X}')
 out.append('')
Path(a.out).write_text('\n'.join(out)+'\n',encoding='utf-8')
print(f'wrote vector candidates to {a.out}')
