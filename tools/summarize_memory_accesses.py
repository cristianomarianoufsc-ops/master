#!/usr/bin/env python3
from pathlib import Path
import argparse,json
p=argparse.ArgumentParser(); p.add_argument('capture',type=Path); p.add_argument('--addresses',required=True); a=p.parse_args()
addresses={f'0x{int(x.strip(),0):04X}' for x in a.addresses.split(',')}
r=json.loads(a.capture.read_text()); print('result',r['result'],'steps',r['steps'],'pc',r['pc'])
for x in r['trace']['records']:
 if x.get('address') in addresses and x.get('kind') in ('mem_read','mem_write'):
  print(x['run'],x['pc'],x['kind'],x['address'],x.get('value'),x['bank_fffe'],x['bank_ffff'], 'regs=',x['a'],x['b'],x['c'],x['d'],x['e'],x['h'],x['l'])
