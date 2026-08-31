#!/usr/bin/env python3
"""Extract consumers of the paged A0 state after the 0x4589 copy."""
import argparse, json
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('trace', type=Path)
p.add_argument('--out', type=Path, required=True)
a=p.parse_args()
d=json.loads(a.trace.read_text())
rows=d.get('trace',{}).get('records',[])
keep=[]
for r in rows:
    addr=r.get('address','')
    if addr in {'0xC0A0','0xC119','0xC11D'} or (addr.startswith('0xC0') and 0xC0E0 <= int(addr,16) <= 0xC0FF):
        keep.append(r)
lines=['# Consumidores do estado A0 após 0x4589','', '| Run | PC | Kind | A | F | BC | DE | HL | Address | Value |','|---:|---|---|---:|---:|---|---|---|---|---:|']
for r in keep:
    lines.append(f"| {r.get('run')} | {r.get('pc')} | {r.get('kind')} | {r.get('a')} | {r.get('f')} | {r.get('b')}/{r.get('c')} | {r.get('d')}/{r.get('e')} | {r.get('h')}/{r.get('l')} | {r.get('address','')} | {r.get('value','')} |")
a.out.write_text('\n'.join(lines)+'\n')
print(f'wrote {a.out}: {len(keep)} rows')
