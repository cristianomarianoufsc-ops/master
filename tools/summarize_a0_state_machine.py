#!/usr/bin/env python3
"""Summarize state transitions in the C0A0-C0A4 scene machine."""
import argparse, json
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('trace', type=Path)
p.add_argument('--out', type=Path, required=True)
a=p.parse_args()
d=json.loads(a.trace.read_text())
rows=d.get('trace',{}).get('records',[])
addresses={'0xC0A0','0xC0A1','0xC0A2','0xC0A3','0xC0A4','0xC112','0xC113','0xC119','0xC11D'}
selected=[r for r in rows if r.get('kind')=='mem_write' and r.get('address') in addresses]
lines=['# Transições da máquina A0/C0A0','','| Run | PC | Address | Value | A | F | D | E | HL |','|---:|---|---|---:|---:|---:|---:|---:|---|']
for r in selected:
    lines.append(f"| {r.get('run')} | {r.get('pc')} | {r.get('address')} | {r.get('value')} | {r.get('a')} | {r.get('f')} | {r.get('d')} | {r.get('e')} | {r.get('h')}/{r.get('l')} |")
a.out.write_text('\n'.join(lines)+'\n')
print(f'wrote {a.out}: {len(selected)} transitions')
