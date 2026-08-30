#!/usr/bin/env python3
from pathlib import Path
import argparse,re

p=argparse.ArgumentParser(description='Track separate FFFE/FFFF page values around selected references')
p.add_argument('asm'); p.add_argument('--out',required=True)
a=p.parse_args(); lines=Path(a.asm).read_text(encoding='utf-8',errors='replace').splitlines()
state={'fffe':None,'ffff':None}; pending=None; rows=[]
for i,line in enumerate(lines):
 m=re.search(r'ld a,0([0-9a-f]+)h',line,re.I)
 if m: pending=int(m.group(1),16)
 for reg in ('fffe','ffff'):
  if pending is not None and re.search(r'ld \(0'+reg+r'h\),a',line,re.I):
   state[reg]=pending; pending=None
 if re.search(r'call 05b3eh|ld de,lad0ch|ld hl,lad0ch',line,re.I):
  rows.append(f'line={i+1} fffe={state["fffe"]} ffff={state["ffff"]} instruction={line.strip()}')
Path(a.out).write_text('# Dual-slot paging contexts\n\n'+'\n'.join(rows)+'\n',encoding='utf-8')
print(f'wrote {len(rows)} contexts to {a.out}')
