#!/usr/bin/env python3
from pathlib import Path
import argparse

p=argparse.ArgumentParser(description='Analyze bank handlers from a vector table at 0x8000')
p.add_argument('rom'); p.add_argument('--bank',type=int,default=22); p.add_argument('--count',type=int,default=32); p.add_argument('--window',type=int,default=96); p.add_argument('--out',required=True)
a=p.parse_args(); rom=Path(a.rom).read_bytes(); data=rom[a.bank*0x4000:(a.bank+1)*0x4000]
out=['# Vector-guided bank analysis','',f'bank={a.bank} vector_cpu=0x8000 count={a.count} window={a.window}','']
seen=set()
for i in range(a.count):
 pos=2*i; pair=data[pos:pos+2]
 if len(pair)<2: break
 target=pair[0]|(pair[1]<<8)
 out.append(f'## vector {i:02X}: target 0x{target:04X}')
 off=target-0x8000
 if not (0<=off<len(data)):
  out.append('outside bank window'); out.append(''); continue
 if target in seen:
  out.append('duplicate target'); out.append(''); continue
 seen.add(target)
 raw=data[off:off+a.window]
 out.append(f'file_offset=0x{a.bank*0x4000+off:X} bytes={raw.hex()}')
 out.append('')
Path(a.out).write_text('\n'.join(out)+'\n',encoding='utf-8')
print(f'wrote {len(seen)} unique vector targets to {a.out}')
