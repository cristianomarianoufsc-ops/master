#!/usr/bin/env python3
from pathlib import Path
import argparse,re

p=argparse.ArgumentParser(description='Resolve paged calls with separate FFFE and FFFF slots')
p.add_argument('asm'); p.add_argument('--out',required=True); p.add_argument('--targets',default='04bbd,04cfd,04d16,05b3e')
a=p.parse_args(); lines=Path(a.asm).read_text(encoding='utf-8',errors='replace').splitlines()
targets={int(x,16) for x in a.targets.split(',')}; state={'fffe':None,'ffff':None}; pending=None; rows=[]
for i,line in enumerate(lines):
 m=re.search(r'ld a,0([0-9a-f]+)h',line,re.I)
 if m: pending=int(m.group(1),16)
 for reg in ('fffe','ffff'):
  if pending is not None and re.search(r'ld \(0'+reg+r'h\),a',line,re.I):
   state[reg]=pending; pending=None
 m=re.search(r'\b(?:call|jp)\s+0?([0-9a-f]+)h',line,re.I)
 if m and int(m.group(1),16) in targets:
  t=int(m.group(1),16)
  rows.append(f'line={i+1} target=0x{t:04X} fffe_bank={state["fffe"]} ffff_bank={state["ffff"]} instruction={line.strip()}')
out=['# Dual-slot call resolution','', 'FFFE controls CPU 4000-7FFF; FFFF controls CPU 8000-BFFF.', '']+rows
Path(a.out).write_text('\n'.join(out)+'\n',encoding='utf-8')
print(f'wrote {len(rows)} call contexts to {a.out}')
