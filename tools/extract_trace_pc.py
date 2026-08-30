#!/usr/bin/env python3
from pathlib import Path
import argparse,json
p=argparse.ArgumentParser(); p.add_argument('trace',type=Path); p.add_argument('--start',type=lambda x:int(x,0),required=True); p.add_argument('--end',type=lambda x:int(x,0),required=True); a=p.parse_args()
r=json.loads(a.trace.read_text());
for x in r.get('trace',{}).get('records',[]):
 pc=int(x.get('pc','0'),0)
 if a.start <= pc <= a.end: print(x)
