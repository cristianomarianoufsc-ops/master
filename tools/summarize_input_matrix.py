#!/usr/bin/env python3
"""Print concise final outcomes from run_input_matrix.py output files."""
from pathlib import Path
import argparse
import json
p=argparse.ArgumentParser()
p.add_argument('matrix', type=Path)
a=p.parse_args()
data=json.loads(a.matrix.read_text())
print('matrix',a.matrix,'press_start',data['press_start'],'press_runs',data['press_runs'])
for item in data['results']:
 print(item['mask'],item['pc'],'FFFF='+str(item['bank_ffff']),'irq='+str(item['irq_count']),'reads='+str(item['controller_reads']))
