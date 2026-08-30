#!/usr/bin/env python3
from pathlib import Path
import argparse
p=argparse.ArgumentParser(description='Analyze internal references in BD55 streams')
p.add_argument('bin');p.add_argument('--out',required=True);p.add_argument('--base',type=lambda x:int(x,16),default=0xbe15)
a=p.parse_args();raw=Path(a.bin).read_bytes();end=raw.find(b'\xff');stream=raw[:end+1] if end>=0 else raw
out=['# BD55 internal reference analysis','',f'input={a.bin} length={len(stream)} base=0x{a.base:04X}','']
for i in range(0,max(0,len(stream)-2)):
 w=stream[i]|stream[i+1]<<8
 if 0x8000<=w<0xc000:
  out.append(f'offset=0x{i:02X} word=0x{w:04X} file_delta=0x{w-a.base:04X}')
out += ['', '## bytes', stream.hex()]
Path(a.out).write_text('\n'.join(out)+'\n',encoding='utf-8');print(f'wrote {a.out}')
