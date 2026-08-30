#!/usr/bin/env python3
from pathlib import Path
import argparse,json
p=argparse.ArgumentParser(); p.add_argument('capture',type=Path); p.add_argument('--start',type=lambda x:int(x,0),required=True); p.add_argument('--end',type=lambda x:int(x,0),required=True); a=p.parse_args()
r=json.loads(a.capture.read_text()); print('result',r['result'],'steps',r['steps'],'pc',r['pc'])
for x in r['trace']['records']:
 if x.get('kind')=='mem_write' and a.start <= int(x.get('address','0'),0) <= a.end:
  print(x['run'],x['pc'],x['address'],x.get('value'),x['bank_fffe'],x['bank_ffff'])
