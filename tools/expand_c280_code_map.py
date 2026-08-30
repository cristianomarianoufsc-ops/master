#!/usr/bin/env python3
from pathlib import Path
import argparse
p=argparse.ArgumentParser(description='Expand C280 acceptance map from D12x bit flags')
p.add_argument('--flags',required=True,help='comma-separated D125..D133 byte values, hex')
p.add_argument('--out',required=True)
a=p.parse_args(); vals=[int(x,16) for x in a.flags.split(',')]
if len(vals)!=9: raise SystemExit('expected 9 bytes D125..D133')
# Conservative model: the 9-byte runtime flag vector forms a 72-bit acceptance table;
# repeat the active 0x20/0x10/0x08 class over code pages for inspection.
active=[]
for i,v in enumerate(vals):
 for bit in range(8):
  if v&(1<<bit): active.append(i*8+bit)
rows=['# Expanded C280 candidate map','',f'flags={a.flags}','active_D12_bits='+','.join(f'{x:02X}' for x in active),'']
for code in range(256):
 # Preserve an auditable heuristic mapping; final runtime map will replace this once D12 state is captured.
 accepted = code in active or (active and (code & 0x1F) in [x & 0x1F for x in active])
 rows.append(f'{code:02X},{1 if accepted else 0}')
Path(a.out).write_text('\n'.join(rows)+'\n',encoding='utf-8');print(f'wrote {a.out}')
