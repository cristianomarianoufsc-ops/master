#!/usr/bin/env python3
from pathlib import Path
import re
import argparse

p=argparse.ArgumentParser(description='Extract data references from dialogue handlers')
p.add_argument('asm');p.add_argument('--out',required=True);p.add_argument('--bank',type=int,default=21)
a=p.parse_args(); lines=Path(a.asm).read_text(errors='replace').splitlines()
handlers={0x9c4f,0x9c78,0x9d22,0x9d4c,0x9d94,0x9e3e,0x9ecf,0xa070,0xa094}
out=['# Dialogue handler candidates','',f'bank={a.bank}','']
for i,line in enumerate(lines):
 m=re.search(r';([0-9a-fA-F]{4})\s*$',line)
 if not m or int(m.group(1),16) not in handlers: continue
 out.append(f'## handler 0x{int(m.group(1),16):04X}')
 for s in lines[max(0,i-8):min(len(lines),i+16)]: out.append(s)
 out.append('')
Path(a.out).write_text('\n'.join(out)+'\n',encoding='utf-8');print(f'wrote {a.out}')
