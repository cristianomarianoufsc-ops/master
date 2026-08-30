#!/usr/bin/env python3
import json
from pathlib import Path
import argparse
p=argparse.ArgumentParser()
p.add_argument('capture', type=Path)
a=p.parse_args()
r=json.loads(a.capture.read_text())
t=r['trace']['records']
dd=[x for x in t if 0xDD00 <= int(x.get('address','0'),0) <= 0xDE37]
print('result',r['result'],'steps',r['steps'],'pc',r['pc'],'trace',len(t),'ddxx',len(dd))
print('dd writes',sum(x['kind']=='mem_write' for x in dd),'dd reads',sum(x['kind']=='mem_read' for x in dd))
print('dd write sample',[(x['run'],x['pc'],x['address'],x['value']) for x in dd if x['kind']=='mem_write'][:40])
print('dd pcs',sorted({x['pc'] for x in dd}))
